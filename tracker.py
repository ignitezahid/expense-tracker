"""Core business logic for expense tracking."""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

from models import Expense
from storage import Storage


class ExpenseTracker:
    """Manages expense operations and reporting."""

    CATEGORIES = [
        "Food", "Transport", "Housing", "Utilities", "Entertainment",
        "Shopping", "Health", "Education", "Travel", "Salary",
        "Investment", "Bills", "Other"
    ]

    def __init__(self, storage: Optional[Storage] = None):
        self.storage = storage or Storage()

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        date: Optional[str] = None,
    ) -> Expense:
        """Add a new expense. Uses today's date if none provided."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        expense = Expense(amount=amount, category=category.capitalize(),
                          description=description, date=date)
        return self.storage.add_expense(expense)

    def get_all_expenses(self) -> List[Expense]:
        """Return all expenses sorted by date (newest first)."""
        expenses = self.storage.get_all_expenses()
        return sorted(expenses, key=lambda e: e.date, reverse=True)

    def get_expense(self, expense_id: int) -> Optional[Expense]:
        """Get a single expense by ID."""
        return self.storage.get_expense_by_id(expense_id)

    def update_expense(self, expense_id: int, **kwargs) -> Optional[Expense]:
        """Update an expense's fields."""
        return self.storage.update_expense(expense_id, **kwargs)

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by ID."""
        return self.storage.delete_expense(expense_id)

    def get_total_spent(self) -> float:
        """Calculate total spending across all expenses."""
        return sum(e.amount for e in self.storage.get_all_expenses())

    def get_category_breakdown(self) -> Dict[str, float]:
        """Return total spent per category."""
        breakdown = defaultdict(float)
        for expense in self.storage.get_all_expenses():
            breakdown[expense.category] += expense.amount
        return dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))

    def get_monthly_summary(self) -> Dict[str, float]:
        """Return total spent per month (YYYY-MM)."""
        summary = defaultdict(float)
        for expense in self.storage.get_all_expenses():
            month_key = expense.date[:7]
            summary[month_key] += expense.amount
        return dict(sorted(summary.items()))

    def get_expenses_by_date_range(
        self, start_date: str, end_date: str
    ) -> List[Expense]:
        """Return expenses within a date range (inclusive)."""
        expenses = self.storage.get_all_expenses()
        return sorted(
            [e for e in expenses if start_date <= e.date <= end_date],
            key=lambda e: e.date,
            reverse=True,
        )

    def get_expenses_by_category(self, category: str) -> List[Expense]:
        """Return all expenses in a given category."""
        return [e for e in self.storage.get_all_expenses()
                if e.category.lower() == category.lower()]

    def export_to_csv(self, filepath: str) -> str:
        """Export all expenses to a CSV file. Returns the filepath."""
        import csv

        expenses = self.storage.get_all_expenses()
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Category", "Description", "Amount"])
            for e in sorted(expenses, key=lambda x: x.date):
                writer.writerow([e.id, e.date, e.category, e.description,
                                f"{e.amount:.2f}"])
        return filepath

    def get_stats(self) -> dict:
        """Return overall statistics."""
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

    # ---- Budget methods ----

    def get_budgets(self) -> Dict[str, float]:
        """Get saved budgets."""
        return self.storage.get_budgets()

    def set_budgets(self, budgets: Dict[str, float]) -> Dict[str, float]:
        """Set and save budgets by category."""
        self.storage.set_budgets(budgets)
        return budgets

    def get_budget_progress(self) -> List[Dict]:
        """Return budget progress for all categories with spending."""
        budgets = self.get_budgets()
        spending = self.get_category_breakdown()
        all_categories = set(list(budgets.keys()) + list(spending.keys()))

        results = []
        for cat in sorted(all_categories):
            spent = spending.get(cat, 0.0)
            budget = budgets.get(cat, 0.0)
            pct = (spent / budget * 100) if budget > 0 else 0
            results.append({
                "category": cat,
                "spent": spent,
                "budget": budget,
                "percent": round(pct, 1),
                "over_budget": pct > 100 if budget > 0 else False,
            })
        return results
