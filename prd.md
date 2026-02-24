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
| `requirements.txt` | Modify | Add dependencies |
| `config.py` | Create | Environment variable configuration |
| `security.py` | Create | JWT validation logic |
| `dependencies.py` | Create | FastAPI dependencies for auth |
| `main.py` | Modify | Add protected routes |
| `.env.example` | Create | Configuration template |

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

## Security Flow

1. Client sends request with `Authorization: Bearer <token>` header
2. `get_token` dependency extracts Bearer token
3. `verify_token` fetches JWKS and validates the token
4. Token is validated against JWKS using RSA256 algorithm
5. Token claims (exp, nbf, iss) are verified
6. If valid, request proceeds; if invalid, 401 is returned

## Error Responses

| Status Code | Description |
|-------------|-------------|
| 401 | Missing/invalid Authorization header or invalid token |
| 500 | JWKS_URI environment variable not configured |

## Verification

1. Set `JWKS_URI` environment variable
2. Start the app: `uvicorn main:app --reload`
3. Test public endpoint (should work without token)
4. Test protected endpoint without token (should return 401)
5. Test protected endpoint with valid token (should return 200)
