# ReWear API Documentation (Current)

Base URL:
`http://localhost:5000/api`

Last updated: March 31, 2026

## Response Contract

Success:
```json
{
  "success": true,
  "message": "...",
  "data": {}
}
```

Failure:
```json
{
  "success": false,
  "message": "...",
  "data": null
}
```

## Authentication

Protected endpoints require:
`Authorization: Bearer <access_token>`

---

## Auth Endpoints

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh-token` (refresh token required)
- `POST /auth/logout`
- `POST /auth/forgot-password`
- `POST /auth/verify-email`

---

## User Endpoints

- `GET /users/me` (protected)
- `GET /users/search` (admin)
- `GET /users` (admin)
- `GET /users/<user_id>`
- `PUT /users/<user_id>` (owner/admin)
- `GET /users/<user_id>/impact`
- `GET /users/<user_id>/impact-history`
- `DELETE /users/<user_id>` (admin; may deactivate if references exist)
- `PUT /users/<user_id>/toggle-status` (admin)

---

## Item Endpoints

- `GET /items`
  - Query params: `page`, `per_page`, `category`, `condition`, `transaction_type`, `search`
- `GET /items/user/<user_id>`
- `POST /items` (protected)
- `GET /items/<item_id>`
- `DELETE /items/<item_id>` (owner)
  - Behavior: hard delete when possible; archive to `inactive` if referenced by transactions

### Create Item Example

```json
{
  "title": "Blue Jacket",
  "description": "Lightly used",
  "category": "tops",
  "size": "M",
  "condition": "good",
  "transaction_type": "buy",
  "price": 35
}
```

---

## Request Endpoints

- `POST /requests` (protected)
  - Supports `rent`, `buy`, `exchange`, `gift`
  - Exchange requires `exchange_item_id`
- `PUT /requests/<request_id>` (protected)
- `GET /requests/user/<sort_type>` (protected, `sent|received`)
- `GET /requests/stats/summary` (protected)
- `GET /requests/<request_id>` (protected)

### Exchange Request Example

```json
{
  "item_id": "<target_item_id>",
  "request_type": "exchange",
  "exchange_item_id": "<your_available_item_id>",
  "message": "Would you like to swap?"
}
```

---

## Order Endpoints

- `POST /orders` (protected)
- `GET /orders/user/<user_id>` (protected, self/admin only)
- `GET /orders/<order_id>` (protected)
- `PUT /orders/<order_id>/status` (protected)
- `GET /orders/stats/summary` (protected)

---

## Impact Endpoints

- `GET /impact/summary`
- `GET /impact/user/<user_id>`
- `GET /impact/me` (protected)
- `GET /impact/monthly`
- `GET /impact/leaderboard`
- `GET /impact/metrics/<user_id>`
- `GET /impact/eco-equivalents/co2/<co2_kg>`
- `GET /impact/eco-equivalents/water/<water_liters>`

---

## Message Endpoints

- `POST /messages` (protected)
- `GET /messages/history/<other_user_id>` (protected)
- `GET /messages/inbox` (protected)

---

## Admin Endpoints

- `GET /admin/dashboard` (admin)
- `PUT /admin/items/<item_id>/moderate` (admin)
- `GET /admin/reported-items` (admin)
- `PUT /admin/users/<user_id>/manage` (admin)
- `GET /admin/requests` (admin)
- `GET /admin/orders` (admin)
- `POST /admin/cleanup` (admin)

---

## HTTP Status Notes

- `200` Success
- `201` Created
- `400` Validation error
- `401` Authentication required/invalid
- `403` Forbidden
- `404` Not found
- `409` Conflict
- `500` Server error

---

## Verification Snapshot

Latest smoke run (March 31, 2026):
- Endpoint checks: 59
- Passed: 59
- Failed: 0

---

## Important Frontend/API Alignment Notes

- Browse transaction filter uses `buy` (not `sell`).
- Exchange request UI expects a selectable `exchange_item_id` from user's available items.
- Item and user delete flows may return successful archive/deactivation instead of hard delete when references exist.
