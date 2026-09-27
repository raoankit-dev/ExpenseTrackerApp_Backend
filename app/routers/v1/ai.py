import sqlite3

from fastapi import APIRouter, Depends

from app.auth.security import get_current_user
from app.database.connection import get_db
from app.schemas.response import DataResponse
from app.services.ai_services import analyze_expenses,chat_with_ai
from app.schemas.ai import AIAnalysis,AIChatRequest,AIChatResponse


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get(
    "/analyze",
    response_model=DataResponse[AIAnalysis],
    summary="Analyze user expenses",
    description="Uses AI to analyze the authenticated user's expenses."
)
def analyze_user_expenses(
    db: sqlite3.Connection = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            title,
            amount,
            category,
            expense_date
        FROM expenses
        WHERE user_id = ?
        ORDER BY expense_date DESC
    """, (user["id"],))

    expenses = cursor.fetchall()

    expense_data = [dict(expense) for expense in expenses]

    analysis = analyze_expenses(expense_data)

    return {
        "success": True,
        "message": "Expense analysis generated successfully",
        "data": analysis
    }


@router.post(
    "/chat",
    response_model=DataResponse[AIChatResponse],
    summary="Ask AI about expenses",
    description="Answers questions about the authenticated user's expenses."
)
def ai_chat(
    chat: AIChatRequest,
    db: sqlite3.Connection = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            title,
            amount,
            category,
            expense_date
        FROM expenses
        WHERE user_id = ?
        ORDER BY expense_date DESC
    """, (user["id"],))

    expenses = cursor.fetchall()

    expense_data = [dict(expense) for expense in expenses]

    answer = chat_with_ai(
        question=chat.question,
        expenses=expense_data
    )

    return {
        "success": True,
        "message": "AI response generated successfully",
        "data": {
            "answer": answer
        }
    }