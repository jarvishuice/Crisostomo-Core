# Infrastructure/Providers/JwtProvider.py
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError

import json
from Config.Settings import Settings
from Domain.Entities.Users.UserEntity import UserEntity
from logging import getLogger
settings = Settings()
log = getLogger(__name__)
class JwtProvider:
    @staticmethod
    def create_token(subject: str) -> str:
        now = datetime.utcnow()
        expire = now + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)

        payload = {
            "sub": json.dumps(subject),
            "iat": now,
            "exp": expire
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
        except ExpiredSignatureError as e:
            log.error("Token vencido ")
            raise e
        except JWTError as e:
            raise e
