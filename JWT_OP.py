from datetime import datetime, timedelta
from typing import Optional
import jwt
from datetime import time
from settings import JWT_SECRET, ALGORITHMS
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer
import jwt


class VerifyToken:
    def __init__(self, token):
        self.token = token

    def verify(self, secret_key, algorithm):
        try:
            decoded_token = jwt.decode(self.token, secret_key, algorithms=[algorithm])
            return decoded_token
        except jwt.exceptions.DecodeError:
            return {"status": False, "msg": "Invalid token"}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    encoded_jwt = jwt.encode(data, JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHMS)

    return token_response(token)


def verify_token(token: HTTPBearer = Depends(HTTPBearer())):
    decoded_token = VerifyToken(token.credentials).verify(JWT_SECRET, ALGORITHMS)
    if decoded_token.get("status"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or authentication required",
        )
    return decoded_token
