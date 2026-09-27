from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class MessageResponse(BaseModel):
    success: bool
    message: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    access_token: str
    token_type: str


class DataResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T


class ListResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: list[T]

class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    expense_date: str
    created_at: str