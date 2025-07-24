from datetime import datetime, timedelta
from jose import jwt
from app.auth.security import verify_password as password_verify
from datetime import datetime, timedelta, timezone
from app.exceptions.customError import CustomError
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")  
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES = os.getenv("EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(password: str, hashed_password: str):
    return password_verify(password, hashed_password)

def create_email_verification_token(email :str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_email_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise CustomError(status_code=400, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise CustomError(status_code=400, detail="Invalid or expired token")
    



    