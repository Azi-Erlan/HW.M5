# Shop API

REST API for an online store built with Django REST Framework.

## Features

* User registration with email confirmation
* JWT authentication and authorization
* Google OAuth 2.0 login
* Product and category management
* Product reviews and ratings
* Custom permission system
* Redis caching
* Background task processing with Celery
* Interactive API documentation with Swagger/OpenAPI

---

## Tech Stack

### Backend

* Python 3.11
* Django
* Django REST Framework

### Database

* PostgreSQL

### Infrastructure

* Docker
* Docker Compose
* Redis
* Celery
* Flower

### Authentication

* JWT Authentication
* Google OAuth 2.0

### Documentation

* Swagger / OpenAPI

---

## Services

The application consists of several services:

* Web (Django + DRF)
* PostgreSQL Database
* Redis Cache
* Celery Worker
* Celery Beat Scheduler
* Flower Monitoring

---

## Project Structure

```text
shop_api/
├── common/
├── product/
├── users/
├── shop_api/
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── manage.py
```

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/Azi-Erlan/shop-api.git
cd shop-api
```

### Create environment variables

Create a `.env` file in the project root and configure:

```env
SECRET_KEY=
DEBUG=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

REDIS_URL=

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

GOOGLE_CLIENT_ID=
```

### Run with Docker

```bash
docker compose up --build
```

### Apply migrations

```bash
docker compose exec web python manage.py migrate
```

### Create superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## API Documentation

Swagger UI:

```text
http://localhost:8000/swagger/
```

Redoc:

```text
http://localhost:8000/redoc/
```

---

## Future Improvements

* Automated tests
* CI/CD pipeline
* Deployment on VPS
* Monitoring and logging

---

## Author

**Erlan Azimkanov**

Junior Python Backend Developer

GitHub:
https://github.com/Azi-Erlan
