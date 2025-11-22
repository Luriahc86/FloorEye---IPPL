from fastapi import Depends, HTTPException
from jose import jwt
from auth_utils import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer

bearer = HTTPBearer()

def get_current_user(token: str = Depends(bearer)):
    try:
        data = jwt.decode(token.credentials, SECRET_KEY, ALGORITHM)
        return data
    except:
        raise HTTPException(401, "Token invalid")


def admin_only(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(403, "Hanya admin yang bisa mengakses")
    return user
