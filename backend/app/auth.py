import time
import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from .config import settings

bearer = HTTPBearer(auto_error=False)
_jwks = {"keys": [], "ts": 0}

async def _get_jwks():
    if time.time() - _jwks["ts"] < 300 and _jwks["keys"]:
        return _jwks
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(f"{settings.keycloak_internal_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs")
        r.raise_for_status()
        data = r.json()
    _jwks.update(keys=data.get("keys", []), ts=time.time())
    return _jwks

async def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    if settings.auth_disabled:
        return {"sub":"dev","preferred_username":"dev","name":"Developer","roles":["admin","manager","user"]}
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization required")
    token = credentials.credentials
    try:
        header = jwt.get_unverified_header(token)
        if header.get("alg") != "RS256":
            raise HTTPException(status_code=401, detail="Unsupported token algorithm")
        jwks = await _get_jwks()
        key = next((k for k in jwks["keys"] if k.get("kid") == header.get("kid")), None)
        if not key:
            raise HTTPException(status_code=401, detail="Unknown signing key")
        payload = jwt.decode(token, key, algorithms=["RS256"], issuer=settings.keycloak_issuer, options={"verify_aud": False})
        if payload.get("azp") not in (None, settings.keycloak_client_id):
            raise HTTPException(status_code=401, detail="Token issued for another client")
        realm_roles = payload.get("realm_access", {}).get("roles", [])
        client_roles = payload.get("resource_access", {}).get(settings.keycloak_client_id, {}).get("roles", [])
        payload["roles"] = sorted(set(realm_roles + client_roles))
        return payload
    except HTTPException:
        raise
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_roles(*roles):
    async def checker(user=Depends(current_user)):
        if settings.auth_disabled:
            return user
        if not set(roles).intersection(user.get("roles", [])):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker
