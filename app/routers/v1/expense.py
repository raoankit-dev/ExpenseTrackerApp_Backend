from fastapi import APIRouter,Depends,HTTPException
from app.schemas.expenses import ExpenseCreate
from app.database.connection import get_db
from app.auth.security import get_current_user
from app.schemas.response import DataResponse,ListResponse,ExpenseResponse,MessageResponse
from datetime import datetime
import sqlite3


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("",response_model=DataResponse[ExpenseResponse])
def create_expense(
    expense : ExpenseCreate, 
    db : sqlite3.Connection = Depends(get_db), 
    user : dict = Depends(get_current_user)
):
    try:
        cursor = db.cursor()

        expense_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO expenses (user_id, title, amount, category, expense_date)
            VALUES (?,?,?,?,?)
        """,(user["id"],expense.title,expense.amount,expense.category,expense_date))

        db.commit()

        expense_id = cursor.lastrowid

        cursor.execute("""
            SELECT id, title, amount, category, expense_date, created_at
            FROM expenses
            WHERE id = ? AND user_id = ?
        """, (expense_id, user["id"]))

        created_expense = cursor.fetchone()

        return {
            "success": True,
            "message": "Expense created successfully",
            "data": dict(created_expense)
        }
    
    except Exception:
        db.rollback()
        raise


@router.get("",response_model=ListResponse[ExpenseResponse])
def get_expense(
    db : sqlite3.Connection = Depends(get_db), 
    user : dict = Depends(get_current_user)
):
    
    try:
        cursor = db.cursor()

        cursor.execute("""
            SELECT id, title, amount, category, expense_date, created_at
            FROM expenses
            WHERE user_id = ?
            ORDER BY id DESC
        """,(user["id"],))

        expenses = cursor.fetchall()

        return {
            "success": True,
            "message": "Expenses fetched successfully",
            "data": [dict(expense) for expense in expenses]
        }
    
    except Exception:
        db.rollback()
        raise
    

@router.get("/{expense_id}",response_model=DataResponse[ExpenseResponse])
def get_expenseBy_id(
    expense_id : int,
    db : sqlite3.Connection = Depends(get_db), 
    user : dict = Depends(get_current_user)
):
    
    try:
        cursor = db.cursor()

        cursor.execute("""
            SELECT id, title, amount, category, expense_date, created_at
            FROM expenses
            WHERE id = ? AND user_id = ? 
        """,(expense_id,user["id"]))

        expense = cursor.fetchone()

        if expense is None:
            raise HTTPException(status_code=404,detail="Expense not found")

        return {
            "success": True,
            "message": "Expense fetched successfully",
            "data": dict(expense)
        }
    
    except Exception:
        db.rollback()
        raise


@router.put("/{expense_id}",response_model=DataResponse[ExpenseResponse])
def update_expense(
    expense_id : int,
    expense: ExpenseCreate,
    db : sqlite3.Connection = Depends(get_db), 
    user : dict = Depends(get_current_user)
):
    
    try:
        cursor = db.cursor()

        expense_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            UPDATE expenses
            SET title = ?,
                amount = ?,
                category = ?,
                expense_date = ?
                WHERE id = ? AND user_id = ?
        """,(
            expense.title,
            expense.amount,
            expense.category,
            expense_date,
            expense_id,
            user["id"]
        ))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404,detail="Expense not found")
        
        db.commit()

        cursor.execute("""
            SELECT id, title, amount, category, expense_date, created_at
            FROM expenses
            WHERE id = ? AND user_id = ?
        """, (expense_id, user["id"]))

        updated_expense = cursor.fetchone()

        return {
            "success": True,
            "message": "Expense updated successfully",
            "data": dict(updated_expense)
        }
    
    except Exception:
        db.rollback()
        raise


@router.delete("/{expense_id}",response_model=MessageResponse)
def delete_expense(
    expense_id : int,
    db : sqlite3.Connection = Depends(get_db), 
    user : dict = Depends(get_current_user)
):
    
    try:
        cursor = db.cursor()

        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ? AND user_id = ?
        """,(expense_id,user["id"]))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404,detail="Expense not found")
        
        db.commit()

        return {
            "success": True,
            "message": "Expense deleted successfully"
        }

    except Exception:
        db.rollback()
        raise