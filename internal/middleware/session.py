import logging
import os
from typing import Optional

import jwt
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def get_jwt_secret() -> str:
    secret = os.getenv("USERS_JWT_SECRET", "")
    if not secret:
        logger.warning("USERS_JWT_SECRET not set; session validation will fail")
    return secret


def validate_session_token(token: str) -> dict:
    """Validate a session JWT token and return its claims."""
    secret = get_jwt_secret()
    if not secret:
        raise HTTPException(status_code=500, detail="session validation not configured")
    try:
        claims = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="session token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid session token")

    if claims.get("type") != "session":
        raise HTTPException(status_code=401, detail="invalid token type")

    return claims


class SessionValidationMiddleware(BaseHTTPMiddleware):
    """Middleware that validates session tokens on protected routes.

    Expects the session token in the X-Session-Token header.
    Adds validated claims to request.state if valid.
    """

    def __init__(self, app, exclude_paths: Optional[list[str]] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/health", "/docs", "/openapi.json"]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        token = request.headers.get("X-Session-Token") or _bearer_token(request)
        if not token:
            return JSONResponse(
                status_code=401,
                content={"error": "missing session token"},
            )

        try:
            claims = validate_session_token(token)
            request.state.user_id = claims.get("sub")
            request.state.session_id = claims.get("sid")
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

        return await call_next(request)


def _bearer_token(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    return ""
