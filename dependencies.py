from fastapi import Request, HTTPException, Depends

from security import fetch_jwks, validate_token
from config import get_jwks_uri


async def get_token(request: Request) -> str:
    """Extract Bearer token from Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return auth_header[7:]


async def verify_token(token: str = Depends(get_token)) -> dict:
    """
    Verify JWT token and return decoded claims.

    Args:
        token: The JWT token extracted from Authorization header

    Returns:
        The decoded token claims

    Raises:
        HTTPException: If token validation fails
    """
    try:
        jwks = await fetch_jwks()
        return validate_token(token, jwks)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
