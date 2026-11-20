# ReWear Quick Reference Guide

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Start backend
python app.py
# Backend running at: http://localhost:5000/api

# 3. Start frontend (new terminal)
cd frontend
python -m http.server 8000
# Frontend at: http://localhost:8000
```

---

## 📁 Essential Files

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask application entry point |
| `backend/models/models.py` | Database models |
| `backend/routes/*.py` | API endpoints (41+) |
| `backend/utils/sustainability.py` | Impact calculations |
| `frontend/index.html` | Landing page |
| `frontend/js/api-client.js` | API communication |
| `.env` | Configuration (copy from .env.example) |

---

## 🔌 API Endpoints Quick Reference

### Auth
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Get JWT tokens |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Invalidate tokens |

### Items
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/items` | List all items |
| POST | `/items` | Upload item |
| GET | `/items/{id}` | Get item details |
| PUT | `/items/{id}` | Update item |
| DELETE | `/items/{id}` | Delete item |

### Users
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/users/{id}` | Get profile |
| PUT | `/users/{id}` | Update profile |
| GET | `/users/{id}/impact` | Get sustainability impact |
| GET | `/users/me` | Get current user |

### Sustainability
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/impact/summary` | Global impact stats |
| GET | `/impact/me` | My impact |
| GET | `/impact/leaderboard` | Eco-champions ranking |
| GET | `/impact/monthly` | Monthly statistics |

### Requests & Orders
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/requests` | Create request |
| PUT | `/requests/{id}` | Update request |
| POST | `/orders` | Create order |
| GET | `/orders/{id}` | Get order details |

---

## 🔑 API Authentication

### Using JWT Token
```javascript
// Get token from login
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
const { data } = await response.json();
const token = data.access_token;

// Use token in requests
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

### Token Expiration
- Access Token: 24 hours
- Refresh Token: 30 days
- Use refresh endpoint to get new access token

---

## 💾 Database Schema Quick Reference

| Table | Contains |
|-------|----------|
| `user` | User accounts, profile info |
| `clothing_item` | Clothing listings, prices |
| `request` | Rent/buy/exchange requests |
| `order` | Completed transactions |
| `impact_metrics` | Sustainability data |
| `review` | Item/user reviews |
| `wishlist` | Saved items |
| `notification` | User notifications |

### Quick SQL Queries
```sql
-- Find user
SELECT * FROM user WHERE email = 'user@example.com';

-- Find available items
SELECT * FROM clothing_item WHERE status = 'available';

-- Check impact stats
SELECT * FROM impact_metrics WHERE user_id = 1;

-- Recent orders
SELECT * FROM order ORDER BY order_date DESC LIMIT 10;
```

---

## 🎨 Frontend Structure

```
frontend/
├── index.html           # Landing page
├── login.html           # Login form
├── register.html        # Registration
├── browse-items.html    # Item browsing
├── dashboard.html       # User dashboard
├── upload-item.html     # Upload items
├── sustainability.html  # Impact dashboard
├── css/
│   └── style.css        # All styling
└── js/
    ├── api-client.js    # API calls
    ├── utils.js         # Utilities
    ├── index.js         # Home page logic
    ├── browse.js        # Browse logic
    ├── dashboard.js     # Dashboard logic
    └── sustainability.js # Impact logic
```

---

## ⚙️ Configuration (.env)

```env
# Server
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///instance/rewear.db

# JWT
JWT_SECRET_KEY=change-me-to-something-super-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRES=86400      # 24 hours
JWT_REFRESH_TOKEN_EXPIRES=2592000   # 30 days

# CORS
FLASK_CORS_ORIGINS=http://localhost:8000

# Sustainability Formulas
CO2_PER_ITEM_KG=3                   # kg
WATER_PER_ITEM_LITERS=7000         # liters
TEXTILE_WASTE_PER_ITEM_KG=0.5      # kg
```

---

## 🧪 Testing Common Scenarios

### Register New User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Password123",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Password123"}'
```

### Get Items
```bash
curl "http://localhost:5000/api/items?category=tops&page=1"
```

### Upload Item
```bash
curl -X POST http://localhost:5000/api/items \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Blue Shirt",
    "category": "tops",
    "size": "M",
    "condition": "good",
    "transaction_type": "sell",
    "price": 15.00
  }'
```

---

## 🐛 Quick Debugging

### Check Backend Status
```bash
curl http://localhost:5000/api/health
```

### Check Database
```bash
sqlite3 instance/rewear.db ".tables"
```

### Clear Browser Cache
```javascript
// Console command
localStorage.clear();
location.reload();
```

### View Server Logs
- Terminal where Flask is running shows all requests/errors

---

## 📊 Common Data Points

### Sustainability Calculations
- CO₂ saved per item: **3 kg**
- Water saved per item: **7,000 liters**
- Textile waste prevented per item: **0.5 kg**

### Eco-Equivalents
- 1 kg CO₂ = 0.0465 trees/year
- 1000L water = 2.64 showers
- 1 L water = 0.0000004 Olympic pools

### Transaction Types
- `rent` - Borrow item
- `sell` - Purchase item
- `exchange` - Trade item
- `free` - Give away

### Item Conditions
- `new`
- `like_new`
- `good`
- `fair`
- `worn`

### Item Categories
- tops
- bottoms
- dresses
- outerwear
- footwear
- accessories

---

## 🎯 Common Tasks

### Change Admin Role
```python
from app import create_app, db
from models.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='admin@example.com').first()
    user.role = 'admin'
    db.session.commit()
```

### Clear Old Data
```python
from app import create_app, db
from models.models import Notification
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    old_date = datetime.now() - timedelta(days=30)
    Notification.query.filter(Notification.created_at < old_date).delete()
    db.session.commit()
```

### Backup Database
```bash
# SQLite
cp instance/rewear.db instance/rewear.db.backup.$(date +%Y%m%d)

# PostgreSQL
pg_dump rewear_production > backup_$(date +%Y%m%d).sql
```

---

## 🔗 Important Links

| Link | Purpose |
|------|---------|
| http://localhost:8000 | Frontend |
| http://localhost:5000/api | API base |
| http://localhost:5000/api-docs | Swagger docs (if enabled) |

---

## 📚 Documentation Files

- `README.md` - Full setup and overview
- `SYSTEM_ARCHITECTURE.md` - Architecture details
- `docs/API_DOCUMENTATION.md` - All API endpoints
- `docs/DEPLOYMENT_GUIDE.md` - Production deployment
- `docs/TROUBLESHOOTING.md` - Common issues
- `DELIVERABLES.md` - Project contents

---

## ⚡ Performance Tips

### Backend
- Use database indexes
- Enable query caching
- Use connection pooling
- Implement pagination

### Frontend
- Lazy load images
- Cache API responses
- Debounce search
- Minimize network requests

### Database
- Regular backups
- VACUUM and ANALYZE
- Monitor query performance
- Clean old data periodically

---

## 🆘 Emergency Reference

**Port already in use?**
```bash
# Mac/Linux
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

**Database corrupted?**
```bash
# Restore backup
cp instance/rewear.db.backup instance/rewear.db

# Or recreate
rm instance/rewear.db
python -c "from app import create_app, db; app = create_app(); db.create_all()"
```

**Token issues?**
```javascript
// Clear storage and logout
localStorage.clear();
location.reload();
```

---

## 📞 Getting Help

1. Check TROUBLESHOOTING.md for your specific error
2. Search error message online
3. Check README.md setup section
4. Review SYSTEM_ARCHITECTURE.md for design
5. Check backend logs in terminal
6. Check browser console (F12)

---

**Last Updated:** December 2024
**Version:** 1.0
