# ReWear System - Troubleshooting Guide

## Common Issues and Solutions

### 🆘 Setup Issues

#### Issue: Python Not Found
**Error:** `'python' is not recognized as an internal or external command`

**Solution:**
1. Install Python 3.8+ from https://www.python.org
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt
4. Verify: `python --version`

#### Issue: Virtual Environment Not Activating
**Error:** `command not found: source` (on Windows)

**Solution:**
- Windows: Use `venv\Scripts\activate.bat` (not `.sh`)
- Mac/Linux: Use `source venv/bin/activate`
- PowerShell: Use `venv\Scripts\Activate.ps1`

#### Issue: pip Install Fails
**Error:** `Permission denied` or `pip: command not found`

**Solution:**
```bash
# Ensure virtual environment is activated
python -m pip install -r requirements.txt  # Instead of pip install

# Or upgrade pip first
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### Issue: ModuleNotFoundError after pip install
**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
1. Verify virtual environment is activated
2. Reinstall requirements:
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```
3. Check Python version compatibility (3.8+)

---

### 🚀 Backend Issues

#### Issue: Flask App Won't Start
**Error:** `Error: While importing "app", an ImportError was raised as follows:`

**Solution:**
1. Ensure you're in the `backend` directory
2. Check `.env` file exists and has required variables
3. Verify database file path is correct
4. Try: `python -c "from app import create_app; app = create_app()"`

#### Issue: "Address already in use" Port Error
**Error:** `OSError: [Errno 48] Address already in use` or `[Errno 98]`

**Solution:**
```bash
# macOS/Linux - Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Windows - Find process using port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F

# Or use different port
python app.py --port 5001
```

#### Issue: Database Connected but Tables Missing
**Error:** `OperationalError: no such table`

**Solution:**
```python
# Initialize database
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Tables created successfully!")
```

#### Issue: JWT Token Errors
**Error:** `422 Unprocessable Entity` or `Signature verification failed`

**Solution:**
1. Verify JWT_SECRET_KEY in `.env` is set
2. Ensure token headers are correct:
   ```
   Authorization: Bearer <token>
   ```
3. Check token hasn't expired (24 hour expiration)
4. Use refresh token to get new access token

#### Issue: CORS Errors
**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
1. Verify Flask-CORS is installed: `pip list | grep Flask-CORS`
2. Check CORS is configured in app.py:
   ```python
   CORS(app, resources={r"/api/*": {"origins": "*"}})
   ```
3. Ensure backend URL in frontend JS matches:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```

#### Issue: Login Works but User Data Doesn't Load
**Error:** `401 Unauthorized` on subsequent requests

**Solution:**
1. Check token is being stored in LocalStorage
2. Verify token format in API calls:
   ```javascript
   headers: {
     'Authorization': `Bearer ${token}`
   }
   ```
3. Check token expiration (24 hours)
4. Try logging out and back in

---

### 🎨 Frontend Issues

#### Issue: Pages Won't Load
**Error:** `404 Not Found` or blank page

**Solution:**
```bash
# Start HTTP server in frontend directory
cd frontend
python -m http.server 8000

# Access via http://localhost:8000
```

#### Issue: Static Assets Not Loading
**Error:** CSS/JS not loading, pages unstyled

**Solution:**
1. Check file paths are correct:
   - `css/style.css` not `css\style.css`
   - Use forward slashes `/` everywhere
2. Verify server is running: `python -m http.server 8000`
3. Check browser cache (Ctrl+Shift+Delete)
4. Check developer console for 404 errors

#### Issue: API Calls Return 404
**Error:** `Failed to fetch`, `404 Not Found`

**Solution:**
1. Verify backend is running on port 5000
2. Check API base URL in `js/api-client.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```
3. Verify endpoint path is correct:
   - Check for typos in endpoint names
   - Verify HTTP method (GET, POST, etc.)

#### Issue: Data Not Displaying After Login
**Error:** Dashboard shows empty, no items load

**Solution:**
1. Check browser console for errors (F12)
2. Verify token is present in LocalStorage
3. Check Network tab to see API responses
4. Ensure API endpoints are returning data
5. Try: `curl http://localhost:5000/api/items`

#### Issue: Form Validation Errors Not Showing
**Error:** Form won't submit, but no error message

**Solution:**
1. Check browser console (F12 → Console)
2. Look at Network tab for what error backend returned
3. Verify validation logic in `utils.js`
4. Check that form inputs have correct `name` attributes

---

### 🗄️ Database Issues

#### Issue: Database File Locked
**Error:** `database is locked` or similar

**Solution:**
1. Ensure only one app instance is running
2. Close any SQLite browsers (DB Browser)
3. Restart Flask app:
   ```bash
   # Kill Flask process and restart
   ```
4. Delete temp files:
   ```bash
   rm -rf instance/__pycache__
   rm -rf build/
   ```

#### Issue: Migration Errors
**Error:** Database schema mismatch

**Solution:**
1. Backup current database:
   ```bash
   cp instance/rewear.db instance/rewear.db.backup
   ```
2. Delete and recreate:
   ```bash
   rm instance/rewear.db
   python -c "from app import create_app, db; app = create_app(); db.create_all()"
   ```

#### Issue: Cannot Insert Data
**Error:** `IntegrityError` or `NOT NULL constraint failed`

**Solution:**
1. Check all required fields are provided
2. Verify data types match schema
3. Check foreign key references exist
4. See specific error message in console

---

### 🔐 Authentication Issues

#### Issue: Cannot Register User
**Error:** `409 Conflict` or `Email already exists`

**Solution:**
1. Use a different email address
2. Reset database if duplicates exist
3. Check email validation regex

#### Issue: Password Reset Not Working
**Error:** Email not received or reset link invalid

**Solution:**
- Email sending not yet implemented (future feature)
- For testing, manually reset in database
- Use admin panel when available

#### Issue: Admin Dashboard Inaccessible
**Error:** `403 Forbidden` when accessing /admin endpoints

**Solution:**
1. Ensure logged-in user has admin role
2. Check user role in database:
   ```sql
   SELECT username, role FROM user WHERE id = 1;
   ```
3. Update role if needed:
   ```sql
   UPDATE user SET role = 'admin' WHERE id = 1;
   ```

---

### 📊 API/Data Issues

#### Issue: No Items Showing in Browse
**Error:** Empty items list despite uploads

**Solution:**
1. Verify items exist in database:
   ```bash
   curl http://localhost:5000/api/items
   ```
2. Check items have `status = 'available'`
3. Check category/filters aren't too restrictive
4. Try uploading a test item

#### Issue: Impact Metrics Not Calculating
**Error:** CO₂ and water saved show 0

**Solution:**
1. Ensure items have transaction types set
2. Check SustainabilityCalculator formulas
3. Verify items have valid conditions
4. Try refreshing page or logout/login

#### Issue: Leaderboard Not Showing Users
**Error:** Empty leaderboard table

**Solution:**
1. Check users have completed transactions
2. Verify impact metrics are calculated
3. Check database has users with impact data
4. Try: `curl http://localhost:5000/api/impact/leaderboard`

---

### 🖥️ Deployment Issues

#### Issue: Application Slow in Production
**Error:** Slow response times, timeouts

**Solution:**
1. Add database indexes:
   ```sql
   CREATE INDEX idx_items_user_id ON clothing_items(user_id);
   CREATE INDEX idx_items_status ON clothing_items(status);
   ```
2. Implement caching for static data
3. Use connection pooling
4. Scale to multiple workers with Gunicorn

#### Issue: Out of Memory Errors
**Error:** `MemoryError` or killed process

**Solution:**
1. Reduce worker processes:
   ```bash
   gunicorn -w 2 app:app  # Instead of 4
   ```
2. Implement pagination for large datasets
3. Add query limits
4. Use database caching

#### Issue: SSL Certificate Errors
**Error:** `CERTIFICATE_VERIFY_FAILED` or HTTPS won't work

**Solution:**
1. Obtain valid SSL certificate
2. Update Nginx configuration with paths
3. Redirect HTTP to HTTPS
4. Test with: `curl -I https://yourdomain.com`

---

### 🎯 Performance Issues

#### Issue: API Response Slow
**Symptom:** API takes >2 seconds to respond

**Solution:**
1. Check database queries:
   - Add indexes on frequently queried columns
   - Use eager loading for relationships
2. Enable query logging:
   ```python
   app.config['SQLALCHEMY_ECHO'] = True
   ```
3. Add caching for expensive operations
4. Use pagination to limit data

#### Issue: Page Load Slow
**Symptom:** Frontend pages take >5 seconds to render

**Solution:**
1. Check Network tab (F12) for slow requests
2. Compress images
3. Minify CSS/JavaScript
4. Implement lazy loading for images
5. Use service workers for caching

---

### 💾 Data/Backup Issues

#### Issue: Lost Data After Crash
**Error:** Data missing or corrupted

**Solution:**
1. Restore from backup:
   ```bash
   cp instance/rewear.db.backup instance/rewear.db
   ```
2. Implement automated backups
3. Set up database replication
4. Use transaction logs

#### Issue: Cannot Export Data
**Error:** Data export fails

**Solution:**
```bash
# Manual export
sqlite3 instance/rewear.db ".dump" > backup.sql

# Or for PostgreSQL
pg_dump rewear_production > backup.sql
```

---

### 🐛 Debug Mode

#### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Check Database Contents
```python
from app import create_app, db
from models.models import User, ClothingItem

app = create_app()
with app.app_context():
    users = User.query.all()
    items = ClothingItem.query.all()
    print(f"Users: {len(users)}, Items: {len(items)}")
```

#### Test API Endpoints
```bash
# Test without authentication
curl http://localhost:5000/api/items

# Test with authentication
curl -H "Authorization: Bearer <token>" \
     http://localhost:5000/api/users/me
```

#### Browser Console Debugging
```javascript
// Check if API client is working
console.log(APIClient);

// Check token in storage
console.log(localStorage.getItem('access_token'));

// Try manual API call
fetch('http://localhost:5000/api/items')
  .then(r => r.json())
  .then(d => console.log(d));
```

---

### 🆘 Still Not Working?

#### Debugging Checklist
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All requirements installed
- [ ] `.env` file configured
- [ ] Backend running on port 5000
- [ ] Frontend running on port 8000
- [ ] Database file exists
- [ ] No port conflicts
- [ ] No firewall blocking
- [ ] Correct file paths
- [ ] Browser console checked for errors
- [ ] Network tab shows API responses

#### Getting Help
1. Check the error message carefully
2. Look at backend logs: `python app.py` (terminal output)
3. Check browser console: F12 → Console
4. Check Network tab: F12 → Network
5. Try the steps in this guide
6. Search error message online
7. Check SYSTEM_ARCHITECTURE.md for design info
8. See README.md for installation details

---

## Performance Optimization Tips

### Backend Optimization
```python
# Use eager loading
items = Item.query.options(joinedload('user')).all()

# Cache expensive queries
from functools import lru_cache

@lru_cache(maxsize=128)
def get_impact_summary(user_id):
    ...
```

### Database Optimization
```sql
-- Add frequently used indexes
CREATE INDEX idx_items_category_status 
ON clothing_items(category, status);

-- Use EXPLAIN to analyze queries
EXPLAIN SELECT * FROM clothing_items 
WHERE category = 'tops' AND status = 'available';
```

### Frontend Optimization
```javascript
// Lazy load images
<img loading="lazy" src="..." />

// Debounce search
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}
```

---

**For additional support, see README.md and SYSTEM_ARCHITECTURE.md**
