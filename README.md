# UniMeal - College Mess Management System (Backend)

A scalable full-stack-ready backend for a **College Mess Management System** supporting:
- **Admin**
- **Hosteller**
- **Day Scholar**

Built with:
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **JWT Auth**
- **Razorpay payment verification hooks**
- **Cloud storage integration points (Cloudinary / AWS S3)**
- **Docker / Docker Compose**

---

## Scalability for ~6500 users

This codebase is designed to comfortably support ~6500 users with:
- Relational schema with indexed lookups (`email`, role, foreign keys).
- Pooled DB connections (`pool_size=30`, `max_overflow=40`).
- Pagination on list-heavy endpoints.
- Modular architecture for horizontal API scaling behind load balancers.

For production at scale, also add:
- Redis caching / rate limiting.
- Background jobs (Celery/RQ) for settlements & notifications.
- Read replicas and observability (Prometheus/Grafana/Sentry).

---

## Project structure

```text
app/
  core/
    config.py
    database.py
    deps.py
    security.py
  models/
    user.py
    qr_code.py
    order.py
    transaction.py
    withdraw_request.py
    base.py
  routers/
    auth.py
    hosteller.py
    day_scholar.py
    admin.py
  schemas/
    user.py
    qr_code.py
    order.py
    withdraw.py
  services/
    payment.py
    storage.py
    wallet.py
  main.py
```

---

## Database schema

Tables included:
1. `users`
2. `qr_codes`
3. `orders`
4. `transactions`
5. `withdraw_requests`

Payment split is enforced in settlement logic:
- ₹65 total
- ₹20 → hosteller wallet
- ₹45 → admin revenue

---

## API features

### Authentication
- Register and login.
- JWT access token.
- Role-based authorization guards.

### Hosteller
- Upload QR code image (cloud upload integration point).
- View uploaded QR codes.
- View sales and earnings summary.
- Raise withdraw requests.

### Day Scholar
- Browse active QR codes.
- Create order for QR purchase (₹65).
- Verify payment signature (Razorpay flow).
- View purchased QR codes.
- View transaction history.

### Admin
- Dashboard metrics (users, uploads, sales, revenue).
- Manage users (activate/deactivate).
- Manage QR codes (activate/deactivate).
- Monitor transactions.
- Approve/reject withdraw requests.

---

## Run locally

### 1) Configure env
```bash
cp .env.example .env
```

### 2) Start using Docker Compose
```bash
docker compose up --build
```

API docs:
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Production hardening checklist

- Replace mocked storage upload logic with real Cloudinary/S3 upload.
- Configure real Razorpay keys and webhook verification.
- Add migrations via Alembic (`alembic revision --autogenerate`).
- Add audit logging and tracing.
- Enforce HTTPS, CORS policy, secure headers.
- Add CI/CD, autoscaling, and secrets manager integration.

---

## Frontend integration guidance

- **Mobile App**: Flutter or React Native consuming `/api/v1` endpoints.
- **Admin Dashboard**: React web app consuming `/api/v1/admin/*` endpoints.
- Use JWT bearer tokens for authenticated API requests.

