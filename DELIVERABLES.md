# ReWear System - Deliverables (Updated)

Last updated: March 31, 2026

## 1) Backend Deliverables

### Core
- `backend/app.py` - Flask app factory, env-based security settings, blueprint wiring
- `backend/database.py` - MongoDB initialization with compatibility export (`db`)
- `backend/config.py` - configuration constants and environment profiles
- `backend/requirements.txt` - backend dependencies

### Data Model Layer
- `backend/models/models.py` - MongoEngine models:
  - User
  - ClothingItem
  - Request
  - Order
  - ImpactMetrics
  - Wishlist
  - Review
  - Notification
  - Message

### Route Layer
- `backend/routes/auth.py`
- `backend/routes/users.py`
- `backend/routes/items.py`
- `backend/routes/requests.py`
- `backend/routes/orders.py`
- `backend/routes/impact.py`
- `backend/routes/messages.py`
- `backend/routes/admin.py`

### Utility Layer
- `backend/utils/auth.py`
- `backend/utils/common.py`
- `backend/utils/sustainability.py`

## 2) Frontend Deliverables

### Pages
- `frontend/index.html`
- `frontend/login.html`
- `frontend/register.html`
- `frontend/browse-items.html`
- `frontend/dashboard.html`
- `frontend/upload-item.html`
- `frontend/sustainability.html`
- `frontend/admin/dashboard.html`

### Scripts
- `frontend/js/api-client.js` - centralized API wrapper and auth header handling
- `frontend/js/utils.js` - UI/Auth helpers + escaping support
- `frontend/js/browse.js` - browse, modal, request flows, exchange offer selector
- `frontend/js/dashboard.js` - profile, requests, impact rendering
- `frontend/js/admin-dashboard.js` - moderation and admin reporting
- `frontend/js/index.js`, `frontend/js/sustainability.js`

### Styling
- `frontend/css/style.css`

## 3) Documentation Deliverables

- `README.md`
- `SYSTEM_ARCHITECTURE.md`
- `QUICK_REFERENCE.md`
- `DOCUMENTATION_INDEX.md`
- `PROJECT_COMPLETE.md`
- `DELIVERABLES.md`
- `docs/API_DOCUMENTATION.md`
- `docs/DEPLOYMENT_GUIDE.md`
- `docs/TROUBLESHOOTING.md`

## 4) Verified Functional Deliverables

The following were validated in smoke tests:

- Authentication flows
- Item create/list/filter/search/details/delete/archive behavior
- User profile/read/update/admin operations
- Request create/list/update/status flows
- Order create/list/read/update/status flows
- Impact summary/leaderboard/equivalents
- Messaging send/history/inbox
- Admin dashboard/moderation/manage/cleanup

Smoke test summary:
- 59 endpoint checks
- 59 passed
- 0 failed

## 5) Notable Fixes Included

- Exchange request UI now loads user's available items for offer selection.
- Deletion operations now degrade safely (archive/deactivate) when references exist.
- API contract standardized for browse/search/user-item retrieval.
- Security posture improved for CORS, JWT, and authz.

## 6) Delivery Status

Status: delivered and verified
Readiness: staging/production candidate
