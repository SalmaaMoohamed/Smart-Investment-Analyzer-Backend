from datetime import datetime, timedelta
from jose import jwt, JWTError

# ===== Secret Key =====
SECRET_KEY = "super_secret_key_change_this"

# ===== Algorithm =====
ALGORITHM = "HS256"

# ===== Expire =====
ACCESS_TOKEN_EXPIRE_DAYS = 90


# ================= CREATE TOKEN =================
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ================= VERIFY TOKEN =================
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