# OAuth2 Resource Server

A FastAPI-based OAuth2 resource server that validates JWT tokens using JWKS (JSON Web Key Set) configuration.

## Overview

This application acts as a protected resource server that:
- Provides a public health/status endpoint accessible without authentication
- Protects API endpoints requiring valid JWT tokens
- Validates JWT signatures against remote JWKS keys
- Implements token caching for improved performance

## Features

- **JWT Validation**: Validates tokens against JWKS endpoints using RS256 algorithm
- **Token Caching**: Caches JWKS for 4 hours to reduce external HTTP calls
- **FastAPI Integration**: Uses FastAPI dependencies for clean authentication flow
- **Automatic Documentation**: Includes Swagger UI at `/docs`

## Project Structure

```
.
├── main.py           # FastAPI application with endpoints
├── security.py       # JWT validation and JWKS fetching logic
├── dependencies.py   # FastAPI dependencies for token extraction/validation
├── config.py         # Environment variable configuration
├── requirements.txt  # Python dependencies
├── .env.example      # Configuration template
├── .env              # Local environment variables (not tracked)
└── prd.md            # Product Requirements Document
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-jose[cryptography]` - JWT token handling
- `httpx` - Async HTTP client for fetching JWKS

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `JWKS_URI` | Yes | The JWKS endpoint URL for token validation (e.g., `https://example.com/.well-known/jwks.json`) |

### Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Update `.env` with your JWKS URI:

```bash
JWKS_URI=https://your-jwks-provider.com/.well-known/jwks.json
```

## API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | No | Public health/status endpoint |
| `/protected` | GET | Yes | Protected endpoint requiring valid JWT |
| `/docs` | GET | No | Swagger UI documentation |

## Usage

### Starting the Server

```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`.

### Testing Endpoints

1. **Public endpoint** (no auth required):
```bash
curl http://localhost:8000/
```

2. **Protected endpoint** without token (returns 401):
```bash
curl http://localhost:8000/protected
```

3. **Protected endpoint** with valid token:
```bash
curl -H "Authorization: Bearer <your-jwt-token>" http://localhost:8000/protected
```

## JWT Validation Flow

1. Client sends request with `Authorization: Bearer <token>` header
2. `get_token` dependency extracts Bearer token from header
3. `verify_token` fetches JWKS (from cache or fresh)
4. Token is validated against JWKS using RS256 algorithm
5. Token claims (`exp`, `nbf`, `iss`) are verified
6. If valid, request proceeds; if invalid, HTTP 401 is returned

## Error Responses

| Status Code | Description |
|-------------|-------------|
| `401` | Missing or invalid Authorization header |
| `401` | Invalid or expired JWT token |
| `500` | JWKS_URI environment variable not configured |

## Development

See `prd.md` for the original Product Requirements Document with detailed specifications.
