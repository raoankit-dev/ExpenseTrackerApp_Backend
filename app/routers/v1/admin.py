import sqlite3

from fastapi import APIRouter,Depends,HTTPException,status
from app.auth.security import get_current_admin
from app.database.connection import get_db


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users")
def get_all_users(
    current_admin: dict = Depends(get_current_admin),
    db : sqlite3.Connection = Depends(get_db)
):

    try:
        cursor = db.cursor()

        cursor.execute("""
            SELECT id, name, email, role
            FROM users
            ORDER BY id
        """)

        users = cursor.fetchall()

        return {
            "success": True,
            "message": "Users fetched successfully",
            "data": [dict(user) for user in users]
        }

    except Exception:
        db.rollback()
        raise


@router.delete("/users/{user_id}")
def delete_user(
    user_id : int,
    current_admin : dict = Depends(get_current_admin),
    db : sqlite3.Connection = Depends(get_db)
):
    
    try:

        cursor = db.cursor()

        cursor.execute("""
            DELETE FROM users
            WHERE id = ?
        """,(user_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404,detail="User not found")
        
        db.commit()

        return {
            "success": True,
            "message": "User deleted successfully"
        }
    
    except Exception:
        db.rollback()
        raise


