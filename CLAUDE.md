# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload

# Run tests (if added)
pytest
```

## Architecture

This is a FastAPI-based OAuth2 resource server with the following structure:

- **main.py**: FastAPI application with two endpoints:
  - `GET /` - Public health/status endpoint (no auth)
  - `GET /protected` - Protected endpoint requiring valid JWT

- **security.py**: Core security logic
  - `fetch_jwks()` - Async JWKS fetching with 4-hour caching (async lock for concurrent requests)
  - `validate_token()` - JWT validation against JWKS keys using RS256

- **dependencies.py**: FastAPI dependencies for authentication flow
  - `get_token()` - Extracts Bearer token from Authorization header
  - `verify_token()` - Full token verification pipeline (depends on security.py)

- **config.py**: Configuration
  - `get_jwks_uri()` - Reads JWKS_URI from environment (raises if not set)

## Key Design Decisions

1. **Async caching**: JWKS is cached for 4 hours with an async lock to prevent concurrent cache refreshes
2. **Dependency chain**: Token extraction (`get_token`) is separate from validation (`verify_token`) for flexibility
3. **Error handling**: Returns HTTP 401 for invalid/missing tokens, HTTP 500 if JWKS_URI not configured
