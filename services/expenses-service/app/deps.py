from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from app.core.config import Config

cfg = Config()
bearer = HTTPBearer(auto_error=True)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(creds.credentials, cfg.JWT_SECRET, algorithms=[cfg.JWT_ALG])
        if "uid" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token (missing uid)")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
