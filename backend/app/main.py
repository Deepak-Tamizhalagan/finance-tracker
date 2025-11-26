from fastapi import FastAPI
from app.router.expenses import router as expenses_router

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "Personal Finance Tracker Backend is running"}

app.include_router(expenses_router)
