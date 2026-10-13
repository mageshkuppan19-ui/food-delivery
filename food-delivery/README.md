# Food Delivery Platform (Backend)

A FastAPI backend for a Zomato/Swiggy/Uber-Eats-style food delivery platform,
with Auth, Users, Restaurants, Menu, Cart, Orders, Payment, Delivery,
Reviews, Notifications (Kafka), and an Admin Dashboard.

## Stack
FastAPI · PostgreSQL (SQLAlchemy) · Redis · Kafka · JWT Auth · Docker

## Run locally with Docker (recommended)

```bash
cp .env.example .env
docker compose up --build
```

API docs: http://localhost:8000/docs

## Run without Docker

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then point DATABASE_URL/REDIS_URL/KAFKA at localhost
uvicorn app.main:app --reload
```

## Project structure

```
food-delivery/
├── app/
│   ├── auth/            # register/login/refresh/logout/forgot/reset
│   ├── users/            # user CRUD, roles
│   ├── restaurants/      # restaurant profile, status, rating
│   ├── menu/              # food CRUD per restaurant
│   ├── cart/              # add/remove/view cart
│   ├── orders/            # place order, track status
│   ├── payment/           # mock cash/UPI/card payments
│   ├── delivery/          # assign + track delivery partner
│   ├── notifications/     # in-app notification feed
│   ├── reviews/           # restaurant + food ratings
│   ├── core/               # settings, security, admin dashboard
│   ├── database/           # SQLAlchemy engine/session
│   ├── middleware/         # JWT auth dependency, role guard
│   ├── schemas/             # Pydantic request/response models
│   ├── models/               # SQLAlchemy ORM tables
│   ├── crud/                  # DB access functions
│   ├── services/               # notification dispatch, business logic
│   ├── kafka/                   # producer/consumer for events
│   └── redis/                    # cache client
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Notes
- Tables auto-create on startup for local dev; swap to Alembic migrations for production.
- `JWT_SECRET_KEY` must be changed before deploying.
- The Kafka consumer (`notification-worker` in docker-compose) turns order events into
  in-app/email/SMS notifications — publish to it from order/delivery routes with
  `app/kafka/producer.py`.
