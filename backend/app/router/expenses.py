from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

# Import from DB setup
from app.database import SessionLocal
from app.models.expense_model import ExpenseDB

router = APIRouter()

# -------------------------------
# 1️⃣ Pydantic Model for Request
# -------------------------------
class Expense(BaseModel):
    title: str
    amount: float
    category: str

# -------------------------------
# 2️⃣ Dependency to get DB session
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# 3️⃣ API → GET /expenses
#    Fetch from DB
# -------------------------------
@router.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseDB).all()
    return expenses

# -------------------------------
# 4️⃣ API → POST /expenses
#    Insert into DB
# -------------------------------
@router.post("/expenses")
def add_expense(expense: Expense, db: Session = Depends(get_db)):
    new_expense = ExpenseDB(
        title=expense.title,
        amount=expense.amount,
        category=expense.category
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return {"message": "Expense added!", "data": expense}

# -------------------------------
# 5️⃣ API → GET /expenses/summary
#    Calculate total from DB
# -------------------------------
@router.get("/expenses/summary")
def get_expenses_summary(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseDB).all()
    total_amount = sum(expense.amount for expense in expenses)
    total_count = len(expenses)
    return {
        "total_count": total_count,
        "total_amount": total_amount
    }

# -------------------------------
# 6️⃣ API → DELETE /expenses/{id}
#    Remove an expense from DB
# -------------------------------
@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()

    if not expense:
        return {"error": "Expense not found"}

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted!"}
