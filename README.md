ve# ReWear Clothing System - Complete Setup Guide

## Project Overview

**ReWear** is a sustainable fashion web-based platform that enables users to reuse, rent, resell, or exchange clothing items. The system promotes environmental sustainability while creating an inclusive fashion community.

### Key Features
✅ User registration and authentication  
✅ Clothing item browsing and searching  
✅ Rent, sell, and exchange functionality  
✅ Environmental impact tracking  
✅ Admin management panel  
✅ Sustainability leaderboard  
✅ Request and order management  

---

## System Architecture

### 3-Layer Architecture

```
Frontend (HTML/CSS/JavaScript)
        ↓ (HTTP/AJAX)
Backend (Flask REST API)
        ↓ (SQL)
Database (PostgreSQL/SQLite)
```

### Technology Stack

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Responsive design
- Local storage for sessions

**Backend:**
- Flask (Python web framework)
- SQLAlchemy ORM
- JWT authentication
- Flask-CORS

**Database:**
- SQLite (development)
- PostgreSQL (production)

---

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js/npm (optional)
- Git
- A code editor (VS Code recommended)

### Step 1: Clone/Extract Project

```bash
cd rewear-system
```

### Step 2: Setup Backend

#### Create Python Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create `.env` file in backend directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///rewear.db
JWT_SECRET_KEY=your-super-secret-key-change-in-production
HOST=0.0.0.0
PORT=5000
```

#### Initialize Database

```bash
python app.py
```

The Flask app will automatically create database tables on first run.

### Step 3: Setup Frontend

No build process needed! The frontend is plain HTML/CSS/JavaScript.

1. Start a simple HTTP server:

**Python 3:**
```bash
cd frontend
python -m http.server 8000
```

**Python 2:**
```bash
cd frontend
python -m SimpleHTTPServer 8000
```

**Or using Node.js:**
```bash
cd frontend
npx http-server -p 8000
```

2. Open in browser: `http://localhost:8000`

### Step 4: Running the Application

**Terminal 1 - Backend (Flask API):**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

**Terminal 2 - Frontend (HTTP Server):**
```bash
cd frontend
python -m http.server 8000
# or using npx http-server
```

### Access Points

- **Frontend:** http://localhost:8000
- **Backend API:** http://localhost:5000/api
- **Health Check:** http://localhost:5000/health

---

## API Endpoints Quick Reference

### Authentication
```
POST   /api/auth/register           Register new user
POST   /api/auth/login              User login
POST   /api/auth/refresh-token      Refresh JWT token
```

### Items
```
GET    /api/items                   Get all items
POST   /api/items                   Upload new item
GET    /api/items/<id>              Get item details
PUT    /api/items/<id>              Update item
DELETE /api/items/<id>              Delete item
GET    /api/items/search            Search items
```

### Users
```
GET    /api/users/<id>              Get user profile
PUT    /api/users/<id>              Update profile
GET    /api/users/<id>/impact       Get user impact
```

### Impact
```
GET    /api/impact/summary          Global impact summary
GET    /api/impact/user/<id>        User impact
GET    /api/impact/leaderboard      Eco-champions leaderboard
```

### Requests
```
POST   /api/requests                Create request
GET    /api/requests/user/sent      Get sent requests
GET    /api/requests/user/received  Get received requests
PUT    /api/requests/<id>           Update request status
```

### Admin
```
GET    /api/admin/dashboard         Admin dashboard
PUT    /api/admin/items/<id>/moderate   Moderate item
GET    /api/admin/requests          All requests
GET    /api/admin/orders            All orders
```

---

## Frontend Pages

### Public Pages
- **index.html** - Landing page with hero section and features
- **login.html** - User login
- **register.html** - User registration
- **browse-items.html** - Browse and search items

### Protected Pages (Login Required)
- **dashboard.html** - User dashboard with profile, items, and requests
- **upload-item.html** - Upload new clothing item
- **sustainability.html** - Environmental impact dashboard and leaderboard

### Admin Pages
- **admin/dashboard.html** - Admin management panel

---

##Sustainability Calculations

### CO₂ Emission Reduction
```
Each item reworn prevents: 3 kg CO₂
Formula: CO₂ saved = items_reworn × 3
```

### Water Saved
```
Each item prevents: 7,000 liters of water
Formula: Water saved = items_involved × 7,000
```

### Environmental Metrics
- **CO₂ Equivalent:** 3 kg CO₂ = 1/22 of annual tree absorption
- **Water Equivalent:** 7,000 liters = 74 showers
- **Textile Waste:** 0.5 kg diverted from landfill per item

---

## Database Schema

### Main Tables

**users** - System users
- id, username, email, password_hash, full_name, mobile, address
- role (user, admin), carbon_saved_kg, water_saved_liters

**clothing_items** - Clothing listings
- id, user_id, title, description, category, size, condition
- transaction_type, price, rental_price_per_day, status
- carbon_impact_kg, water_impact_liters

**requests** - Transaction requests
- id, item_id, requester_id, owner_id, request_type, status
- message, rental_days, exchange_item_id

**orders** - Completed transactions
- id, request_id, item_id, buyer_id, seller_id, order_type
- total_amount, status, delivery_address, tracking_number

**impact_metrics** - Sustainability logging
- id, user_id, item_id, action_type
- co2_reduced_kg, water_saved_liters

---

## Authentication & Security

### JWT Token
```json
{
  "iss": "rewear-system",
  "sub": "user_id",
  "role": "user|admin",
  "iat": 1234567890,
  "exp": 1234571490
}
```

### Security Features
- Password hashing with bcrypt
- JWT-based authentication
- CORS protection
- Input validation and sanitization
- SQL injection prevention via parameterized queries

### Token Expiration
- Access Token: 24 hours
- Refresh Token: 30 days

---

## User Roles

### Regular User
- Browse and search items
- Upload items for rental/sale/exchange
- Place requests for items
- View personal impact metrics
- Manage profile

### Admin
- View all users and content
- Moderate items and requests
- Access system analytics
- Manage user accounts
- View global impact statistics

---

## Testing the System

### Test Credentials (After Setup)

Register new account through registration page, or use:
- **Email:** testuser@rewear.com
- **Password:** TestPassword123

### Test Workflow

1. **Register Account**
   - Go to http://localhost:8000/register.html
   - Fill in registration form

2. **Login**
   - Navigate to login page
   - Enter credentials

3. **Upload Item**
   - Click "Upload Item" from dashboard
   - Fill item details
   - Submit

4. **Browse Items**
   - Go to Browse page
   - Search or filter items
   - Click "Request" to create request

5. **View Impact**
   - Go to Sustainability page
   - View personal and global impact
   - Check leaderboard

---

## Common Issues & Solutions

### Issue: "Database is locked"
**Solution:** Make sure only one instance of Flask is running. Kill any existing processes:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue: CORS errors when frontend calls API
**Solution:** Ensure backend is running and frontend is correctly configured:
- Check API_BASE_URL in js/api-client.js
- Verify backend is running on port 5000
- Check Flask-CORS is initialized

### Issue: "Module not found" errors
**Solution:** Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Port already in use
**Solution:** Use different port:
```bash
# Backend (use PORT env variable)
PORT=5001 python app.py

# Frontend
python -m http.server 8001
```

---

## Project Structure

```
rewear-system/
├── backend/
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration
│   ├── models/
│   │   └── models.py          # SQLAlchemy models
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User management
│   │   ├── items.py           # Item management
│   │   ├── requests.py        # Request endpoints
│   │   ├── orders.py          # Order endpoints
│   │   ├── impact.py          # Sustainability endpoints
│   │   └── admin.py           # Admin endpoints
│   ├── utils/
│   │   ├── auth.py            # Auth helpers
│   │   ├── sustainability.py  # Impact calculations
│   │   └── common.py          # Common utilities
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
│
├── frontend/
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── browse-items.html      # Browse items
│   ├── dashboard.html         # User dashboard
│   ├── upload-item.html       # Upload item
│   ├── sustainability.html    # Impact dashboard
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   ├── api-client.js      # API handler
│   │   ├── utils.js           # Utility functions
│   │   ├── index.js           # Home page script
│   │   ├── browse.js          # Browse page script
│   │   ├── dashboard.js       # Dashboard script
│   │   └── sustainability.js  # Impact page script
│   └── admin/                 # Admin pages
│
├── database/
│   └── schema.sql             # Database schema
│
├── docs/
│   ├── SYSTEM_ARCHITECTURE.md # Architecture
│   └── API_DOCUMENTATION.md   # API docs
│
└── README.md                  # This file
```

---

## Deployment

### Production Deployment Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Change `JWT_SECRET_KEY` to strong random value
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL
- [ ] Set up email for notifications
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Use production WSGI server (Gunicorn)

### Deploy with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment (Optional)

Create `Dockerfile` for containerization.

---

## Contributing Guidelines

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## Performance Optimization Tips

- Enable database query caching
- Optimize image sizes before upload
- Implement pagination for large datasets
- Use CDN for static assets
- Enable gzip compression
- Minify CSS and JavaScript

---

## Future Enhancements

- [ ] Real-time notifications
- [ ] Payment gateway integration
- [ ] Mobile app (React Native)
- [ ] Machine learning for recommendations
- [ ] Social features (follow, messaging)
- [ ] AR try-on feature
- [ ] Blockchain for supply chain tracking
- [ ] Integration with thrift stores

---

## Support & Contact

- **Email:** support@rewear.com
- **Issues:** GitHub Issues
- **Documentation:** See `/docs` folder

---

## License

This project is part of an academic mini-project for IT 6th Semester.

---

## Acknowledgments

- Environmental impact data sourced from leading sustainability research
- UI/UX inspired by modern e-commerce platforms
- Built with open-source technologies

---

## Version History

- **v1.0** (March 2026) - Initial release
  - Core functionality complete
  - 3-tier architecture implemented
  - Sustainability tracking active
  - Admin panel functional

---

**Happy Sustainable Shopping! ♻️**

For detailed API documentation, see `API_DOCUMENTATION.md`
