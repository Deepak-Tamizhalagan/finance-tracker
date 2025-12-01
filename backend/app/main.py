from fastapi import FastAPI
from app.router.expenses import router as expenses_router

# NEW IMPORTS FOR DB
from app.database import Base, engine
from app.models.expense_model import ExpenseDB

app = FastAPI()

# NEW LINE: Create the tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"message": "Personal Finance Tracker Backend is running"}

app.include_router(expenses_router)
