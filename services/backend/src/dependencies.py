import asyncio
from typing import Annotated

import httpx
from authlib.jose import JsonWebToken, KeySet
from authlib.jose.errors import JoseError
from cachetools import TTLCache, cached
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import CONFIG

bearer_scheme: HTTPBearer = HTTPBearer()

jwt = JsonWebToken(["RS256"])

jwks_cache: TTLCache = TTLCache(maxsize=20, ttl=3600)


class JWKSCache(TTLCache):
    @staticmethod
    async def _get_jwks(url: str) -> KeySet:
        if CONFIG.oidc is None:
            raise ValueError("OIDC not configured.")
        async with httpx.AsyncClient() as client:
            response = await client.get(str(CONFIG.oidc.jwks_uri))
            response.raise_for_status()

            return KeySet(response.json())

    def __missing__(self, url: str):
        fut: asyncio.Task = asyncio.create_task(self._get_jwks(url))
        self[url] = fut
        return fut


# This will eventually be replaced with OIDC to integrate with the
# rest of it all, but just so I can post on the devlog for now
def verify_token(authorization: Annotated[str, Header()] = None):  # pyright: ignore [reportArgumentType]
    if CONFIG.api.recovery_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No auth methods allowed."
        )
    elif authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided."
        )
    auth_parts: list[str] = authorization.split(" ")
    if auth_parts[0].lower() != "bearer" or len(auth_parts) < 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth method."
        )
    if auth_parts[1] != CONFIG.api.recovery_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
