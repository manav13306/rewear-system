# ReWear Deployment Guide

## Production Deployment Checklist

### Pre-Deployment

- [ ] Update `.env` with production settings
- [ ] Set `FLASK_ENV=production`
- [ ] Generate strong `JWT_SECRET_KEY`
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up SSL certificates
- [ ] Configure domain name DNS
- [ ] Prepare hosting environment

### Database Migration

```bash
# Backup development database
cp instance/rewear.db instance/rewear.db.backup

# Create production database schema
python -c "from app import create_app, db; app = create_app('production'); db.create_all()"
```

### Environment Configuration

**Production .env:**
```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/rewear_prod
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRES=86400
JWT_REFRESH_TOKEN_EXPIRES=2592000
FLASK_CORS_ORIGINS=https://yourdomain.com
```

### Running with Production Server

#### Option 1: Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run application
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

**Recommended settings for production:**
```bash
gunicorn -w 4 \
  -b 0.0.0.0:5000 \
  --timeout 120 \
  --access-logfile /var/log/rewear/access.log \
  --error-logfile /var/log/rewear/error.log \
  --log-level info \
  app:app
```

#### Option 2: uWSGI

```bash
# Install uWSGI
pip install uwsgi

# Run application
uwsgi --socket 0.0.0.0:5000 --protocol=http -w app:app
```

### Nginx Configuration

```nginx
upstream rewear_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://rewear_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/rewear/frontend;
    }
}
```

### Docker Deployment

#### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .
COPY frontend/ /app/frontend

# Set environment
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  rewear-db:
    image: postgres:13
    environment:
      POSTGRES_USER: rewear_user
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: rewear_production
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  rewear-app:
    build: .
    environment:
      DATABASE_URL: postgresql://rewear_user:secure_password@rewear-db:5432/rewear_production
      FLASK_ENV: production
      JWT_SECRET_KEY: your-secret-key
    ports:
      - "5000:5000"
    depends_on:
      - rewear-db
    volumes:
      - ./backend:/app

  rewear-nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - rewear-app

volumes:
  postgres_data:
```

**Deploy with Docker Compose:**
```bash
docker-compose up -d
```

### Performance Optimization

#### Database Optimization

```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_items_user_id ON clothing_items(user_id);
CREATE INDEX idx_items_category ON clothing_items(category);
CREATE INDEX idx_items_status ON clothing_items(status);
CREATE INDEX idx_requests_status ON requests(status);
CREATE INDEX idx_orders_user_id ON orders(buyer_id, seller_id);
```

#### Caching Setup

```python
# Add Redis caching to app.py
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis',
                           'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

# Cache global impact for 1 hour
@app.route('/api/impact/summary')
@cache.cached(timeout=3600)
def get_global_impact():
    ...
```

#### Load Balancing

For high traffic, use Nginx with multiple Gunicorn workers:
```bash
# Terminal 1
gunicorn -w 2 -b 127.0.0.1:5001 app:app

# Terminal 2
gunicorn -w 2 -b 127.0.0.1:5002 app:app

# Nginx upstream config
upstream rewear_app {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}
```

### Monitoring & Logging

#### Application Monitoring

```bash
# Install monitoring tools
pip install prometheus-flask-exporter

# Add to app.py
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
```

#### Log Rotation

```bash
# /etc/logrotate.d/rewear
/var/log/rewear/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
```

### Security Hardening

1. **HTTPS Only**
```python
@app.after_request
def set_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

2. **Rate Limiting**
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/auth/login')
@limiter.limit("5 per minute")
def login():
    ...
```

3. **WAF Configuration**
- Use Cloudflare or AWS WAF
- Block common attack patterns
- Monitor for suspicious activity

### Database Backup Strategy

```bash
#!/bin/bash
# Daily backup script
BACKUP_DIR="/backups/rewear"
DATE=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump rewear_production > $BACKUP_DIR/rewear_$DATE.sql

# Compress
gzip $BACKUP_DIR/rewear_$DATE.sql

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/rewear_$DATE.sql.gz s3://rewear-backups/

# Keep only last 30 days
find $BACKUP_DIR -name "rewear_*.sql.gz" -mtime +30 -delete
```

### Systemd Service File

Create `/etc/systemd/system/rewear.service`:

```ini
[Unit]
Description=ReWear Clothing System
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/rewear
ExecStart=/var/www/rewear/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable rewear
sudo systemctl start rewear
sudo systemctl status rewear
```

### Monitoring Checklist

- [ ] Set up application logging
- [ ] Configure error tracking (Sentry)
- [ ] Set up performance monitoring
- [ ] Configure uptime monitoring
- [ ] Set up alerts for high error rates
- [ ] Monitor database performance
- [ ] Track API response times
- [ ] Monitor server resources

### Post-Deployment

1. Test all critical user flows
2. Verify database backups working
3. Set up monitoring alerts
4. Document deployment process
5. Create runbooks for common issues
6. Set up team access controls
7. Schedule regular security updates
8. Monitor user feedback

---

## Rollback Procedure

```bash
# If deployment fails:
# 1. Restore database
psql rewear_production < /backups/rewear/rewear_backup.sql

# 2. Rollback code
git revert <commit_hash>

# 3. Restart service
sudo systemctl restart rewear

# 4. Verify
curl http://localhost:5000/api/health
```

---

For more information, see README.md and SYSTEM_ARCHITECTURE.md
