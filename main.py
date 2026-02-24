from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from dependencies import verify_token

app = FastAPI()


@app.get("/")
async def root():
    """Public health/status endpoint."""
    return {"message": "Hello World - Public Endpoint"}


@app.get("/protected")
async def protected(token: dict = Depends(verify_token)):
    """Protected endpoint requiring valid JWT token."""
    return {"message": "Protected endpoint", "token": token}
