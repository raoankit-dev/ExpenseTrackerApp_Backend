from fastapi import APIRouter,Depends
import sqlite3
from app.database.connection import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("")
def health_check():
    return {
        "status":"healthy"
    }


@router.get("/database")
def database_check(
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )

    tables = cursor.fetchall()

    return {
        "database": "connected",
        "tables": [table["name"] for table in tables]
    }