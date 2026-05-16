# auth_utils.py

from datetime import datetime, timedelta
from jose import JWTError, jwt

# SECRET KEY
SECRET_KEY = "SMART_INVESTMENT_SECRET_KEY"

# ALGORITHM
ALGORITHM = "HS256"

# Expire after 90 days
ACCESS_TOKEN_EXPIRE_DAYS = 90


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None