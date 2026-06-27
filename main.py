from fastapi import FastAPI
from pydantic import BaseModel
from collections import defaultdict

app = FastAPI()
expenses = []


class Expense(BaseModel):
    payer: str
    amount: float
    participants: list[str]


@app.post("/expense")
def add_expense(e: Expense):
    expenses.append(e)
    return {"status": "recorded", "count": len(expenses)}


@app.get("/balances")
def balances():
    net = defaultdict(float)
    for e in expenses:
        share = e.amount / len(e.participants)
        for p in e.participants:
            net[p] -= share
        net[e.payer] += e.amount
    return {k: round(v, 2) for k, v in net.items()}
