# Product Requirements Document (PRD)

## Overview
Secure the FastAPI hello world application as an OAuth2 resource server to validate JWT tokens using a JWKS URI configuration.

## Requirements Summary

| Requirement | Description |
|-------------|-------------|
| JWKS Configuration | Configure JWKS URI via environment variable |
| Token Validation | Verify JWT signatures against JWKS keys |
| Protected Endpoints | Require valid Bearer token in Authorization header |
| Public Endpoints | Some endpoints remain accessible without authentication |

## Technical Specifications

### Dependencies
- `python-jose[cryptography]` - JWT token validation
- `httpx` - Async HTTP client for fetching JWKS

### Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `requirements.txt` | Modified | Added python-jose[cryptography] and httpx |
| `config.py` | Created | Environment variable configuration for JWKS_URI |
| `security.py` | Created | JWT validation with JWKS fetching and 4-hour caching |
| `dependencies.py` | Created | FastAPI dependencies for token extraction/validation |
| `main.py` | Modified | Added public and protected endpoints |
| `.env.example` | Created | Configuration template |
| `.env` | Created | Local environment variables with real JWKS URI |

### API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | No | Public health/status endpoint |
| `/protected` | GET | Yes | Protected endpoint requiring valid JWT |
| `/docs` | GET | No | Swagger UI documentation |

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `JWKS_URI` | Yes | The JWKS endpoint for token validation |

### Example `.env` File
```bash
JWKS_URI=https://example.com/.well-known/jwks.json
```

### Real JWKS URI (for testing)
```bash
JWKS_URI=https://javed-ameen-shaikh.github.io/mock-jwks/jwks.json
```

## Security Flow

1. Client sends request with `Authorization: Bearer <token>` header
2. `get_token` dependency extracts Bearer token from header
3. `verify_token` fetches JWKS (from 4-hour cache or fresh fetch)
4. Token is validated against JWKS using RS256 algorithm
5. Token claims (`exp`, `nbf`, `iss`) are verified
6. If valid, request proceeds; if invalid, HTTP 401 is returned

## Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | Missing or invalid Authorization header |
| 401 | Invalid or expired JWT token |
| 500 | JWKS_URI environment variable not configured |

## Features

- **JWT Validation**: Validates tokens against JWKS endpoints using RS256 algorithm
- **Token Caching**: Caches JWKS for 4 hours to reduce external HTTP calls
- **FastAPI Integration**: Uses FastAPI dependencies for clean authentication flow
- **Automatic Documentation**: Includes Swagger UI at `/docs`

## Verification

1. Ensure `JWKS_URI` is set in `.env` file
2. Start the app: `uvicorn main:app --reload`
3. Test public endpoint (should return 200 without token)
4. Test protected endpoint without token (should return 401)
5. Test protected endpoint with valid token (should return 200)

## Development

The project includes a mock JWKS provider at `https://javed-ameen-shaikh.github.io/mock-jwks/jwks.json` for testing.
