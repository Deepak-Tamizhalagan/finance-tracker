from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Expense(BaseModel):
    id: int
    title: str
    amount: float
    category: str

# Temporary example data 
expenses_data = [
    Expense(id=1, title="Groceries", amount=50.75, category="Food"),
    Expense(id=2, title="Uber Ride", amount=18.00, category="Transport"),
]

@router.get("/expenses")
def get_expenses():
    return expenses_data

@router.post("/expenses")
def add_expense(expense: Expense):
    expenses_data.append(expense)
    return {"message": "Expense added!", "data": expense}
