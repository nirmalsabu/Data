# Intelligent Book Management System

This project provides a modular FastAPI-based book management service with:

- Async SQLAlchemy database access
- JWT-based authentication
- Book CRUD operations
- Review collection and summary support
- Modular services for future Llama-style AI integration
- Unit tests for core CRUD and auth behavior

## Project structure

- app/api/routes: API endpoint modules
- app/core: settings and dependency wiring
- app/db: database models and CRUD logic
- app/schemas: request and response models
- app/services: summary and AI-related services
- tests/unit: automated unit tests

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run locally

Start the API:

```bash
uvicorn main:app --reload
```

Open:

- http://127.0.0.1:8000/docs for Swagger UI
- http://127.0.0.1:8000/redoc for ReDoc

## Authentication

1. Register a user at POST /auth/register
2. Login at POST /auth/login to receive a JWT token
3. Use the token in the Authorization header as Bearer token

## Example endpoints

- POST /books
- GET /books
- GET /books/{id}
- PUT /books/{id}
- DELETE /books/{id}
- POST /books/{id}/reviews
- GET /books/{id}/reviews
- GET /books/{id}/summary
- GET /recommendations
- POST /generate-summary

## Testing

Run tests:

```bash
pytest -q
```

## Docker deployment

Build and run with Docker Compose:

```bash
docker compose up --build
```

## Cloud deployment path

This service is structured so it can be deployed to a cloud platform such as Render, Railway, Azure App Service, or AWS ECS. The current local setup uses SQLite for simplicity, and the config layer is already isolated so it can be swapped to PostgreSQL in production.
