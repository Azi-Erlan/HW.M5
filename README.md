# Shop API

REST API интернет-магазина, разработанный на Django REST Framework.

## Технологии

* Python 3.11
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* JWT Authentication
* Google OAuth 2.0
* Docker
* Docker Compose
* Swagger/OpenAPI

## Возможности

* Регистрация пользователей
* Подтверждение аккаунта по email
* JWT-аутентификация
* Авторизация через Google
* Категории товаров
* Товары
* Отзывы
* Кастомные права доступа
* Кэширование через Redis
* Асинхронные задачи через Celery
* Документация API через Swagger

## Запуск проекта

```bash
git clone <repo_url>
cd shop-api

docker compose up --build
```

## API Документация

Swagger:

```text
http://localhost:8000/swagger/
```

## Автор

Эрлан Азимканов

Junior Python Backend Developer
