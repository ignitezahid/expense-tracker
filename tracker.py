"""Core business logic."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from models import Expense
from storage import Storage


class ExpenseTracker:
    CATEGORIES = [
        "Food", "Transport", "Housing", "Utilities", "Entertainment",
        "Shopping", "Health", "Education", "Travel", "Salary",
        "Investment", "Bills", "Other"
    ]

    def __init__(self, storage: Storage | None = None):
        self.storage = storage or Storage()

    def add_expense(self, amount, category, description, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        expense = Expense(amount=amount, category=category.capitalize(),
                          description=description, date=date)
        return self.storage.add_expense(expense)

    def get_all_expenses(self):
        return sorted(self.storage.get_all_expenses(),
                      key=lambda e: e.date, reverse=True)

    def get_expense(self, expense_id):
        return self.storage.get_expense_by_id(expense_id)

    def update_expense(self, expense_id, **kwargs):
        return self.storage.update_expense(expense_id, **kwargs)

    def delete_expense(self, expense_id):
        return self.storage.delete_expense(expense_id)

    def get_total_spent(self):
        return sum(e.amount for e in self.storage.get_all_expenses())

    def get_category_breakdown(self):
        b = defaultdict(float)
        for e in self.storage.get_all_expenses():
            b[e.category] += e.amount
        return dict(sorted(b.items(), key=lambda x: x[1], reverse=True))

    def get_monthly_summary(self):
        s = defaultdict(float)
        for e in self.storage.get_all_expenses():
            s[e.date[:7]] += e.amount
        return dict(sorted(s.items()))

    def get_expenses_by_date_range(self, start, end):
        ex = self.storage.get_all_expenses()
        return sorted([e for e in ex if start <= e.date <= end],
                      key=lambda e: e.date, reverse=True)

    def get_expenses_by_category(self, category):
        return [e for e in self.storage.get_all_expenses()
                if e.category.lower() == category.lower()]

    def export_to_csv(self, filepath):
        import csv
        expenses = self.storage.get_all_expenses()
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Date", "Category", "Description", "Amount"])
            for e in sorted(expenses, key=lambda x: x.date):
                w.writerow([e.id, e.date, e.category, e.description,
                           f"{e.amount:.2f}"])
        return filepath

    def get_stats(self):
        expenses = self.storage.get_all_expenses()
        if not expenses:
            return {"count": 0, "total": 0, "average": 0,
                    "max": None, "min": None, "categories": 0}
        amounts = [e.amount for e in expenses]
        return {
            "count": len(expenses),
            "total": sum(amounts),
            "average": sum(amounts) / len(amounts),
            "max": max(amounts),
            "min": min(amounts),
            "categories": len(set(e.category for e in expenses)),
        }

    def get_budgets(self):
        return self.storage.get_budgets()

    def set_budgets(self, budgets):
        self.storage.set_budgets(budgets)
        return budgets

    def get_budget_progress(self):
        budgets = self.get_budgets()
        spending = self.get_category_breakdown()
        cats = set(list(budgets.keys()) + list(spending.keys()))
        results = []
        for cat in sorted(cats):
            spent = spending.get(cat, 0.0)
            budget = budgets.get(cat, 0.0)
            pct = (spent / budget * 100) if budget > 0 else 0
            results.append({
                "category": cat, "spent": spent, "budget": budget,
                "percent": round(pct, 1),
                "over_budget": pct > 100 if budget > 0 else False,
            })
        return results
