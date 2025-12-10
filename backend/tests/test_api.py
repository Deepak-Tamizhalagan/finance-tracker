# backend/tests/test_api.py

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Make sure the backend root (where app/ lives) is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.main import app
from app.database import Base, engine
from app.models.expense_model import ExpenseDB

client = TestClient(app)



@pytest.fixture(autouse=True)
def reset_db():
    """
    Before each test:
    - Drop all tables
    - Recreate tables

    This keeps tests isolated and avoids leftover data.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # (No cleanup needed after tests right now)


def test_health_check_root():
    """GET / should return a health message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Personal Finance Tracker" in data["message"]


def test_get_expenses_initially_empty():
    """Initially, /expenses should return an empty list."""
    response = client.get("/expenses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_add_expense_and_list():
    """POST /expenses should insert an expense that appears in GET /expenses."""
    payload = {
        "title": "Groceries",
        "amount": 50.0,
        "category": "Food",
    }
    create_resp = client.post("/expenses", json=payload)
    assert create_resp.status_code == 200
    create_data = create_resp.json()
    assert create_data["message"] == "Expense added!"

    list_resp = client.get("/expenses")
    assert list_resp.status_code == 200
    expenses = list_resp.json()
    assert len(expenses) == 1
    assert expenses[0]["title"] == "Groceries"
    assert expenses[0]["amount"] == 50.0
    assert expenses[0]["category"] == "Food"


def test_expenses_summary_matches_data():
    """Summary endpoint should return correct total_count and total_amount."""
    # Add two expenses
    client.post("/expenses", json={"title": "Rent", "amount": 1000.0, "category": "Housing"})
    client.post("/expenses", json={"title": "Coffee", "amount": 5.0, "category": "Food"})

    summary_resp = client.get("/expenses/summary")
    assert summary_resp.status_code == 200
    summary = summary_resp.json()

    assert summary["total_count"] == 2
    # Floating point: allow tiny difference
    assert abs(summary["total_amount"] - 1005.0) < 0.0001


def test_delete_expense_removes_record():
    """DELETE /expenses/{id} should remove an existing expense."""
    # Add an expense
    client.post("/expenses", json={"title": "Movie", "amount": 15.0, "category": "Entertainment"})

    # Fetch to get its ID
    list_resp = client.get("/expenses")
    expenses = list_resp.json()
    assert len(expenses) == 1
    expense_id = expenses[0]["id"]

    # Delete it
    del_resp = client.delete(f"/expenses/{expense_id}")
    assert del_resp.status_code == 200
    del_data = del_resp.json()
    assert del_data["message"] == "Expense deleted!"

    # Confirm list is empty
    list_resp_after = client.get("/expenses")
    expenses_after = list_resp_after.json()
    assert len(expenses_after) == 0
