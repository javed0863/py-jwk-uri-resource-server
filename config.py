import os


def get_jwks_uri() -> str:
    """Get the JWKS URI from environment variable."""
    jwks_uri = os.getenv("JWKS_URI")
    if not jwks_uri:
        raise ValueError("JWKS_URI environment variable is not configured")
    return jwks_uri
