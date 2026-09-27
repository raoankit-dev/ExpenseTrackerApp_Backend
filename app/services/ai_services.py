import os
import json
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_expenses(expenses: list[dict]):

    expense_text = "\n".join(
        [
            f"Title: {expense['title']}, "
            f"Amount: {expense['amount']}, "
            f"Category: {expense['category']}, "
            f"Date: {expense['expense_date']}"
            for expense in expenses
        ]
    )

    prompt = f"""
You are a personal finance assistant.

Analyze the following expense data.

{expense_text}

Provide:
1. A short spending summary.
2. The highest spending category.
3. Important spending patterns.
4. Three practical suggestions to manage spending.

Keep the response simple and useful.
Do not invent any financial data that is not present.
"""

    response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": """
You are a personal finance assistant.

Analyze the user's expense data and return ONLY valid JSON.

The JSON must have exactly these fields:

{
    "summary": "string",
    "highest_spending_category": "string",
    "patterns": ["string"],
    "suggestions": ["string"]
}

Do not use Markdown.
Do not add extra fields.
Do not invent financial data.

All monetary amounts are in Indian Rupees (INR/₹).
Always display monetary amounts using ₹.
Never use $, USD, or any other currency symbol.
"""
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.3
)

    content = response.choices[0].message.content

    return json.loads(content)

def chat_with_ai(
    question: str,
    expenses: list[dict]
) -> str:

    expense_text = "\n".join(
        [
            f"Title: {expense['title']}, "
            f"Amount: {expense['amount']}, "
            f"Category: {expense['category']}, "
            f"Date: {expense['expense_date']}"
            for expense in expenses
        ]
    )

    prompt = f"""
The user is asking a question about their expenses.

Expense data:

{expense_text}

User question:
{question}

Answer the user's question only if it is related to
their expenses, spending, budgets, or financial patterns.

If it is unrelated, use the exact refusal message
specified in the system instructions.

All monetary amounts must be displayed in ₹.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
    "role": "system",
    "content": """
You are an expense analysis assistant built specifically for an Expense Tracker application.

Your ONLY purpose is to help the user understand and manage their expenses.

You can answer questions about:
- User's expenses
- Spending
- Categories
- Spending patterns
- Budgets
- Saving suggestions related to their expenses
- Daily, monthly, and yearly spending
- Expense-related calculations

You MUST NOT answer general knowledge questions,
politics, news, entertainment, coding questions,
or questions unrelated to personal expense management.

If the user's question is unrelated to expenses, respond exactly with:

"I'm your expense analysis assistant. I can only help you with your expenses, spending, budgets, and financial patterns."

All monetary amounts are in Indian Rupees (INR).
Always display monetary amounts using ₹.
Never use $, USD, or another currency symbol.

Use only the expense data provided by the application.
Never invent expense data.
"""
},
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content