import httpx
import asyncio
from jose import jwt, JWTError
from datetime import datetime, timedelta

from config import get_jwks_uri

# Cache variables
_cache = {
    "data": None,
    "expiry": None,
    "lock": None
}


def _get_cache_lock():
    """Get or create the cache lock."""
    global _cache
    if _cache["lock"] is None:
        _cache["lock"] = asyncio.Lock()
    return _cache["lock"]


async def fetch_jwks() -> dict:
    """Fetch JWKS from the configured JWKS URI with 4-hour caching."""
    global _cache

    now = datetime.utcnow()
    cache_lock = _get_cache_lock()

    async with cache_lock:
        # Check if cache is valid
        if _cache["data"] is not None and _cache["expiry"] is not None and now < _cache["expiry"]:
            return _cache["data"]

        # Cache invalid or expired, fetch new JWKS
        jwks_uri = get_jwks_uri()
        async with httpx.AsyncClient() as client:
            response = await client.get(jwks_uri)
            response.raise_for_status()
            jwks_data = response.json()

        # Update cache with 4-hour expiry
        _cache["data"] = jwks_data
        _cache["expiry"] = now + timedelta(hours=4)

        return jwks_data


def validate_token(token: str, jwks: dict) -> dict:
    """
    Validate JWT token against JWKS keys.

    Args:
        token: The JWT token to validate
        jwks: The JWKS dictionary containing public keys

    Returns:
        The decoded token claims

    Raises:
        JWTError: If token validation fails
    """
    # Decode header to get key id
    header = jwt.get_unverified_header(token)

    # Find matching key in JWKS
    key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
    if not key:
        raise JWTError("Key not found in JWKS")

    # Decode and validate token
    return jwt.decode(token, key, algorithms=["RS256"], options={"verify_aud": False})
