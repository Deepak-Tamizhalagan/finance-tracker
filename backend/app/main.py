from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.expenses import router as expenses_router

# NEW IMPORTS FOR DB
from app.database import Base, engine
from app.models.expense_model import ExpenseDB

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NEW LINE: Create the tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"message": "Personal Finance Tracker Backend is running"}

app.include_router(expenses_router)
