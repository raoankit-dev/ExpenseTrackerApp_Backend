import sqlite3
from fastapi import APIRouter,Depends,HTTPException
from app.database.connection import get_db
from app.auth.security import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard_statics(db : sqlite3.Connection = Depends(get_db),user : dict = Depends(get_current_user)):
    
    try:
        cursor = db.cursor()

        cursor.execute("""
            SELECT 
                COUNT(*) AS expense_count,
                COALESCE(SUM(amount), 0) AS total_amount,
                COALESCE(AVG(amount), 0) AS average_amount
            FROM expenses
            WHERE user_id = ?
        """,(user["id"],))

        result = cursor.fetchone()

        cursor.execute("""
            SELECT category,
                       SUM(amount) AS total
                       FROM expenses
                       WHERE user_id = ? 
                       GROUP BY category
        """,(user["id"],))

        category_expense = cursor.fetchall()

        cursor.execute("""
            SELECT 
                COALESCE(SUM(amount), 0) AS today_expense
            FROM expenses
            WHERE user_id = ?
            AND expense_date = DATE("now")
        """,(user["id"],))

        today_exp = cursor.fetchone()

        cursor.execute("""
            SELECT 
                COALESCE(SUM(amount), 0) AS monthly_expense
            FROM expenses
            WHERE user_id = ?
            AND strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
        """,(user["id"],))

        monthly_exp = cursor.fetchone()

        cursor.execute("""
            SELECT 
                COALESCE(SUM(amount), 0) AS yearly_expense
            FROM expenses
            WHERE user_id = ?
            AND strftime('%Y', expense_date) = strftime('%Y', 'now')
        """,(user["id"],))

        yearly_exp = cursor.fetchone()

        return {
            "user_name" : user["name"],
            "expenses" : dict(result),
            "today" : dict(today_exp),
            "monthly" : dict(monthly_exp),
            "yearly" : dict(yearly_exp),
            "category" : [dict(row) for row in category_expense]
        }
    
    except Exception:
        db.rollback()
        raise