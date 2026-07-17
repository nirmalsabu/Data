# Intelligent Book Management System

This project provides a modular FastAPI-based book management service with:

- Async SQLAlchemy database access
- Authentication and JWT-based login
- Book CRUD operations
- Review management
- Summary generation hooks for Llama-style models
- Unit tests for core CRUD and auth modules

## Project structure

- app/api/routes: API endpoints
- app/core: application configuration and dependency wiring
- app/db: database models and CRUD modules
- app/schemas: request and response schemas
- app/services: AI/summary-related logic
- tests/unit: unit tests

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

Then browse to:

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

## Testing

Run tests:

```bash
pytest -q
```

## Cloud deployment note

The API is designed to be deployed to a cloud platform such as Render, Railway, or Azure App Service. In this starter version, it uses SQLite for local development while remaining ready to switch to PostgreSQL in production.
