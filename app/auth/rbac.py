from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, APIKeyHeader
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
import hashlib
from app.core.db import get_async_session
from app.config import settings

bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_current_context(
    credentials = Security(bearer),
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    tenant_id, role = None, "user"
    if api_key:
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        stmt = text("SELECT tenant_id, role FROM api_keys WHERE key_hash = :hash AND active = true")
        res = await session.execute(stmt, {"hash": key_hash})
        row = res.first()
        if not row: raise HTTPException(401, "Invalid API key")
        tenant_id, role = row
    elif credentials:
        try:
            payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=["HS256"])
            tenant_id, role = f"tenant_{payload['sub']}", payload.get("role", "user")
        except JWTError:
            raise HTTPException(401, "Invalid token")
    else:
        raise HTTPException(401, "Missing auth")
    return {"tenant_id": tenant_id, "role": role}