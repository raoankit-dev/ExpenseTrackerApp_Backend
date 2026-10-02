import os
import jwt
import sqlite3
from dotenv import load_dotenv
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException,status
from app.database.connection import get_db

ph = PasswordHash.recommended()

def hash_password(password : str) -> str:
    return ph.hash(password)

def verify_password(
        plain_password :str,
        hashed_password : str
) -> bool:
    return ph.verify(plain_password,hashed_password)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

# Code to generate token...
def create_access_token(user_id: int, role : str):

    payload = {
        "sub" : str(user_id),
        "role" : role
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm
    )

    return token


#Code to verify token...
def verify_token(token: str):
    try: 
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithm
        )
        return payload
    except jwt.InvalidTokenError:
        return None
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token : str = Depends(oauth2_scheme),db : sqlite3.Connection = Depends(get_db)):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401,detail="Invalid token")

    
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, email, role FROM users WHERE id = ?
    """,(int(user_id),))


    user = cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=401,detail="User not found")
    
    return dict(user)


def get_current_admin(admin : dict = Depends(get_current_user)):

    if admin["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return admin