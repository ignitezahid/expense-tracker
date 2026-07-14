"""JSON-based file storage for expenses and budgets."""

import json
import os
from typing import Dict, List, Optional

from models import Expense


DEFAULT_DATA_FILE = "expenses.json"


class Storage:
    """Handles reading and writing data to a JSON file."""

    def __init__(self, filepath: str = DEFAULT_DATA_FILE):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        """Create the data file if it doesn't exist."""
        if not os.path.exists(self.filepath):
            self._write_raw({"expenses": [], "budgets": {}})

    def _read_raw(self) -> dict:
        """Read the full data structure from JSON.
        Auto-migrates old flat-list format to new dict format.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Migration: old format was just a list of expenses
            if isinstance(data, list):
                data = {"expenses": data, "budgets": {}}
                self._write_raw(data)
            return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {"expenses": [], "budgets": {}}

    def _write_raw(self, data: dict):
        """Write the full data structure to JSON."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # ---- Expense methods ----

    def add_expense(self, expense: Expense) -> Expense:
        """Add a new expense and return it with an assigned ID."""
        data = self._read_raw()
        expenses = data["expenses"]
        expense.id = (max(e["id"] for e in expenses) + 1) if expenses else 1
        expenses.append(expense.to_dict())
        data["expenses"] = expenses
        self._write_raw(data)
        return expense

    def get_all_expenses(self) -> List[Expense]:
        """Return all expenses as Expense objects."""
        data = self._read_raw()
        return [Expense.from_dict(item) for item in data["expenses"]]

    def get_expense_by_id(self, expense_id: int) -> Optional[Expense]:
        """Find an expense by its ID."""
        for item in self._read_raw()["expenses"]:
            if item["id"] == expense_id:
                return Expense.from_dict(item)
        return None

    def update_expense(self, expense_id: int, **kwargs) -> Optional[Expense]:
        """Update fields of an expense by ID. Returns updated expense or None."""
        data = self._read_raw()
        for i, item in enumerate(data["expenses"]):
            if item["id"] == expense_id:
                for key, value in kwargs.items():
                    if value is not None and key in item:
                        item[key] = value
                data["expenses"][i] = item
                self._write_raw(data)
                return Expense.from_dict(item)
        return None

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by ID. Returns True if deleted."""
        data = self._read_raw()
        before = len(data["expenses"])
        data["expenses"] = [e for e in data["expenses"] if e["id"] != expense_id]
        if len(data["expenses"]) == before:
            return False
        self._write_raw(data)
        return True

    def clear_all_expenses(self):
        """Delete all expenses (keeps budgets)."""
        data = self._read_raw()
        data["expenses"] = []
        self._write_raw(data)

    # ---- Budget methods ----

    def get_budgets(self) -> Dict[str, float]:
        """Return all budgets as {category: amount}."""
        return self._read_raw().get("budgets", {})

    def set_budgets(self, budgets: Dict[str, float]):
        """Replace all budgets."""
        data = self._read_raw()
        data["budgets"] = budgets
        self._write_raw(data)
