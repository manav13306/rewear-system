# ReWear Clothing System - Architecture Documentation

## Project Overview
ReWear is a sustainable fashion web-based platform that enables users to reuse, rent, resell, or exchange clothing items. This system promotes environmental sustainability while creating an inclusive fashion community.

---

## System Architecture

### 3-Tier Architecture Design

```
┌─────────────────────────────────────────────────┐
│        PRESENTATION LAYER (Frontend)            │
│  HTML, CSS, JavaScript - User Interface         │
│  - User Pages                                   │
│  - Admin Dashboard                              │
│  - Search & Browse Interface                    │
└────────────┬────────────────────────────────────┘
             │ HTTP/AJAX Requests
             ▼
┌─────────────────────────────────────────────────┐
│      APPLICATION LAYER (Backend - Flask API)    │
│  RESTful Web Services & Business Logic           │
│  - User Management                              │
│  - Authentication & Authorization               │
│  - Clothing Item Management                     │
│  - Request Processing (Rent/Sell/Exchange)      │
│  - Sustainability Calculations                  │
│  - Order Management                             │
└────────────┬────────────────────────────────────┘
             │ SQL Queries
             ▼
┌─────────────────────────────────────────────────┐
│        DATA LAYER (MongoDB/PostgreSQL)          │
│  Database - Data Persistence                    │
│  - Users Table                                  │
│  - Clothing Items Table                         │
│  - Requests Table                               │
│  - Orders Table                                 │
│  - Impact Metrics Table                         │
└─────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design with Flexbox/Grid
- **JavaScript (Vanilla)**: DOM manipulation, API calls
- **Local Storage**: Session management

### Backend
- **Framework**: Flask (Python)
- **Authentication**: JWT (JSON Web Tokens)
- **Database ORM**: SQLAlchemy
- **Validation**: Marshmallow
- **Password Hashing**: bcrypt

### Database
- **Primary**: PostgreSQL / SQLite (for simplicity in development)
- **Alternative**: MongoDB with Mongoose

### Tools & Libraries
- **API Testing**: Postman
- **Version Control**: Git
- **Environment Management**: python-dotenv

---

## Core Features

### 1. User Management
- User Registration with email validation
- Secure Login with JWT authentication
- Role-based access control (User, Admin)
- User Profile management
- Carbon footprint tracking per user

### 2. Clothing Item Management
- Upload items with image, category, size, condition
- Track rewear count
- Display item availability status
- Search and filtering capabilities

### 3. Transaction Management
- Place rent requests
- Initiate sales
- Process exchanges
- View request history
- Order tracking

### 4. Sustainability Metrics
- CO₂ emission reduction calculation
- Water saved estimation
- Environmental impact dashboard
- User contribution statistics

### 5. Admin Dashboard
- User management
- Item moderation
- Transaction oversight
- System analytics

---

## REST API Endpoints

### Authentication
```
POST   /api/auth/register          - User registration
POST   /api/auth/login             - User login
POST   /api/auth/logout            - User logout
POST   /api/auth/refresh-token     - Refresh JWT token
```

### User Management
```
GET    /api/users/<id>             - Get user profile
PUT    /api/users/<id>             - Update user profile
GET    /api/users/<id>/impact      - Get user sustainability impact
GET    /api/users                  - List all users (Admin only)
DELETE /api/users/<id>             - Delete user (Admin only)
```

### Clothing Items
```
POST   /api/items                  - Upload new clothing item
GET    /api/items                  - Browse all items
GET    /api/items/<id>             - Get item details
PUT    /api/items/<id>             - Update item
DELETE /api/items/<id>             - Delete item
GET    /api/items/search           - Search items with filters
GET    /api/items/category/<cat>   - Browse by category
```

### Requests Management
```
POST   /api/requests               - Create rewear/rent/exchange request
GET    /api/requests/<id>          - Get request details
PUT    /api/requests/<id>          - Update request status
GET    /api/requests/user/<uid>    - Get user's requests
GET    /api/requests               - List all requests (Admin)
```

### Orders & History
```
POST   /api/orders                 - Create order
GET    /api/orders/<uid>           - Get user's order history
GET    /api/orders/<oid>           - Get order details
```

### Sustainability
```
GET    /api/impact/summary         - Global impact summary
GET    /api/impact/user/<uid>      - User-specific impact
GET    /api/impact/monthly         - Monthly statistics
```

---

## Database Schema Overview

### Users Table
```sql
id (PK) | username | email | password_hash | full_name | 
mobile | address | role | carbon_saved | water_saved | 
items_reworn | items_rented | created_at | updated_at
```

### Clothing_Items Table
```sql
id (PK) | user_id (FK) | title | description | category | 
size | condition | rewear_count | image_url | status | 
transaction_type | price | created_at | updated_at
```

### Requests Table
```sql
id (PK) | item_id (FK) | requester_id (FK) | owner_id (FK) | 
request_type | status | message | created_at | updated_at
```

### Orders Table
```sql
id (PK) | request_id (FK) | buyer_id (FK) | seller_id (FK) | 
total_amount | status | delivery_address | created_at | delivered_at
```

### Impact_Metrics Table
```sql
id (PK) | user_id (FK) | action_type | co2_reduced | 
water_saved | timestamp
```

---

## Authentication & Authorization

### JWT Token Structure
```json
{
  "iss": "rewear-system",
  "sub": "user_id",
  "role": "user|admin",
  "iat": 1234567890,
  "exp": 1234571490
}
```

### Role-Based Access Control
- **User**: Can create items, request items, view own data
- **Admin**: Can manage all users, moderate items, view analytics

### Security Features
- Password hashing with bcrypt
- HTTPS for all API calls
- JWT token expiration (24 hours)
- CORS protection
- Input validation and sanitization

---

## Sustainability Calculation Logic

### CO₂ Emission Reduction
```
Each clothing item reworn prevents:
- Manufacturing: 2.5 kg CO₂
- Transportation: 0.5 kg CO₂
- Total per item: 3 kg CO₂

Formula: co2_saved = rewear_count × 3
```

### Water Saved
```
Producing one clothing item requires ~7,000 liters of water

Formula: water_saved = items_rented × 7000 liters
```

### Environmental Impact Score
```
Impact Score = (CO₂ saved / 3) × 10 + (Water saved / 7000) × 5
```

---

## Project Structure
```
rewear-system/
├── backend/
│   ├── app.py                    # Flask app initialization
│   ├── config.py                 # Configuration settings
│   ├── requirements.txt           # Python dependencies
│   ├── models/                    # Database models
│   ├── routes/                    # API endpoints
│   ├── utils/                     # Helper functions
│   └── middleware/                # Authentication, logging
├── frontend/
│   ├── index.html                 # Landing page
│   ├── register.html              # Registration page
│   ├── login.html                 # Login page
│   ├── dashboard.html             # User dashboard
│   ├── browse-items.html          # Browse items
│   ├── impact.html                # Sustainability dashboard
│   ├── admin/                     # Admin pages
│   ├── css/                       # Stylesheets
│   └── js/                        # JavaScript files
├── database/
│   ├── schema.sql                 # Database schema
│   └── migrations/                # Migration files
├── docs/
│   └── API_DOCUMENTATION.md       # API details
└── README.md                      # Project overview
```

---

## Development Workflow

### Setup & Installation
1. Clone repository
2. Create Python virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure database connection
5. Run migrations: `flask db upgrade`
6. Start Flask server: `python app.py`
7. Open frontend in browser: `http://localhost:5000`

### Testing Workflow
- Test API with Postman
- Use browser DevTools for frontend debugging
- Use Flask logging for backend debugging

---

## Security Considerations

1. **Input Validation**: Validate all user inputs
2. **SQL Injection Prevention**: Use parameterized queries
3. **XSS Prevention**: Sanitize JavaScript outputs
4. **CSRF Protection**: Implement token validation
5. **Rate Limiting**: Prevent API abuse
6. **Data Encryption**: Store sensitive data encrypted

---

## Scalability & Performance

### Current Phase (MVP)
- Single server deployment
- SQLite/PostgreSQL database
- In-memory caching

### Future Improvements
- Microservices architecture
- Load balancing with Nginx
- Redis caching
- CDN for image delivery
- Database replication

---

## Sustainability Impact Metrics

The system tracks and promotes environmental benefits:
- **CO₂ Reduction**: Equivalent to tree plantation
- **Water Conservation**: Measured in liters saved
- **Textile Waste Prevention**: Number of items diverted from landfills
- **User Contribution**: Leaderboard of eco-conscious users

---

## Success Criteria

✅ Fully functional 3-tier architecture
✅ Secure authentication system
✅ Complete CRUD operations for all resources
✅ Accurate sustainability calculations
✅ Intuitive user interface
✅ Admin management capabilities
✅ Well-documented codebase
✅ Ready for academic evaluation

---

*Last Updated: March 2026*
*Version: 1.0*
