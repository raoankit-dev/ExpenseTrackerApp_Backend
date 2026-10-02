import os
from dotenv import load_dotenv
from fastapi import APIRouter,Depends, HTTPException
from app.schemas.user import UserCreate,UserLogin
import sqlite3
from app.auth.security import hash_password, verify_password,create_access_token, get_current_user
from app.database.connection import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.response import MessageResponse,LoginResponse,DataResponse

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",status_code=201,response_model=MessageResponse)
def user_register(user : UserCreate,db : sqlite3.Connection = Depends(get_db)):

    cursor = db.cursor()

    cursor.execute("""
        SELECT id FROM users
        WHERE email = ?
    """,(user.email,))

    user_exists = cursor.fetchone()

    if user_exists:
        raise HTTPException(status_code=409,detail="User already exists with this email")
    
    password_hash = hash_password(user.password)

    cursor.execute("""
        INSERT INTO users (name,email,password_hash)
        VALUES (?,?,?)
    """,(user.name,user.email,password_hash))

    db.commit()

    return {
        "success": True,
        "message": "User registered successfully"
    }


@router.post("/login",status_code=201,response_model=LoginResponse)
def user_login(
    user : UserLogin, 
    # user: OAuth2PasswordRequestForm = Depends(), #After testing make thsi comment and the comment part make user..
    db : sqlite3.Connection = Depends(get_db)
):

    cursor = db.cursor()

    cursor.execute("""
        SELECT id FROM users
        WHERE email = ?
    """,(user.email,)) # change username to email.

    user_exists = cursor.fetchone()

    if user_exists is None:
        raise HTTPException(status_code=401,detail="email or password invalid")
    
    
    cursor.execute("""
        SELECT * 
        FROM users
        WHERE email = ?
    """,(user.email,)) # change username to email.

    existing_user = cursor.fetchone()
    
    is_valid_password = verify_password(user.password,existing_user["password_hash"])

    if not is_valid_password:
        raise HTTPException(status_code=401,detail="email or password invalid")

    role = existing_user["role"]
    if ADMIN_EMAIL and user.username.strip().lower() == ADMIN_EMAIL.strip().lower():
        role = "admin"
        cursor.execute("""
            UPDATE users
            SET role = 'admin'
            WHERE id = ?
        """,(existing_user["id"],))
        db.commit()
    
    token = create_access_token(existing_user["id"],role)


    return {
        "success": True,
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }
    

    
@router.get("/me",response_model=DataResponse[dict])
def get_me(current_user : dict = Depends(get_current_user)):

    return {
    "success": True,
    "message": "Current user fetched successfully",
    "data": current_user
}
