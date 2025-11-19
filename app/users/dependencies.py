from fastapi import Request, HTTPException, Depends
import jwt
from app.config import settings
from datetime import datetime, timezone
from app.users.dao import UserDAO
from fastapi import status


def get_token(request: Request):
    token = request.cookies.get('auth_test_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
        token, settings.JWT_KEY, settings.ALGORITHM
    )
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await UserDAO.find_by_id(user_id)
    if not user:
        return False
    return user
