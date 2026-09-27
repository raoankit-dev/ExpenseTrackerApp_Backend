from pydantic import BaseModel,Field


class ExpenseCreate(BaseModel):
    title : str = Field(min_length=2,max_length=50)
    amount : float = Field(gt=0)
    category : str = Field(min_length=2,max_length=50)


