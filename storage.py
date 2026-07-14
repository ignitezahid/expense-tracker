"""JSON file storage."""
import json
import os

from models import Expense

DATA_FILE = "expenses.json"


class Storage:
    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({"expenses": [], "budgets": {}}, f, indent=2)

    def _read(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"expenses": [], "budgets": {}}

    def _write(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_expense(self, expense):
        data = self._read()
        expenses = data["expenses"]
        expense.id = (max(e["id"] for e in expenses) + 1) if expenses else 1
        expenses.append(expense.to_dict())
        data["expenses"] = expenses
        self._write(data)
        return expense

    def get_all_expenses(self):
        data = self._read()
        return [Expense.from_dict(item) for item in data["expenses"]]

    def get_expense_by_id(self, expense_id):
        for item in self._read()["expenses"]:
            if item["id"] == expense_id:
                return Expense.from_dict(item)
        return None

    def update_expense(self, expense_id, **kwargs):
        data = self._read()
        for i, item in enumerate(data["expenses"]):
            if item["id"] == expense_id:
                for k, v in kwargs.items():
                    if v is not None and k in item:
                        item[k] = v
                data["expenses"][i] = item
                self._write(data)
                return Expense.from_dict(item)
        return None

    def delete_expense(self, expense_id):
        data = self._read()
        before = len(data["expenses"])
        data["expenses"] = [e for e in data["expenses"] if e["id"] != expense_id]
        if len(data["expenses"]) == before:
            return False
        self._write(data)
        return True

    def clear_all_expenses(self):
        data = self._read()
        data["expenses"] = []
        self._write(data)

    def get_budgets(self):
        return self._read().get("budgets", {})

    def set_budgets(self, budgets):
        data = self._read()
        data["budgets"] = budgets
        self._write(data)
