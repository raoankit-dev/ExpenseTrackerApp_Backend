from pydantic import BaseModel,Field


class AIAnalysis(BaseModel):
    summary: str
    highest_spending_category: str
    patterns: list[str]
    suggestions: list[str]

class AIChatRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=500
    )


class AIChatResponse(BaseModel):
    answer: str