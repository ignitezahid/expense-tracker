"""Tests for the Personal Expense Tracker."""

import os
import tempfile
import unittest

from models import Expense
from storage import Storage
from tracker import ExpenseTracker


class TestExpenseModel(unittest.TestCase):
    """Tests for the Expense data model."""

    def test_valid_expense(self):
        expense = Expense(amount=25.50, category="Food",
                          description="Lunch", date="2024-01-15")
        self.assertEqual(expense.amount, 25.50)
        self.assertEqual(expense.category, "Food")

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            Expense(amount=-10, category="Food",
                    description="Test", date="2024-01-15")

    def test_empty_category(self):
        with self.assertRaises(ValueError):
            Expense(amount=10, category="",
                    description="Test", date="2024-01-15")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            Expense(amount=10, category="Food",
                    description="Test", date="not-a-date")

    def test_to_dict(self):
        expense = Expense(id=1, amount=10.0, category="Food",
                          description="Snack", date="2024-01-15")
        d = expense.to_dict()
        self.assertEqual(d["id"], 1)
        self.assertEqual(d["amount"], 10.0)
        self.assertEqual(d["category"], "Food")

    def test_from_dict(self):
        data = {"id": 1, "amount": 10.0, "category": "Food",
                "description": "Snack", "date": "2024-01-15"}
        expense = Expense.from_dict(data)
        self.assertEqual(expense.id, 1)
        self.assertEqual(expense.amount, 10.0)


class TestStorage(unittest.TestCase):
    """Tests for JSON Storage."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        self.storage = Storage(self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_add_and_get(self):
        expense = Expense(amount=10, category="Food",
                          description="Snack", date="2024-01-15")
        saved = self.storage.add_expense(expense)
        self.assertIsNotNone(saved.id)

        all_expenses = self.storage.get_all_expenses()
        self.assertEqual(len(all_expenses), 1)
        self.assertEqual(all_expenses[0].amount, 10)

    def test_get_by_id(self):
        expense = self.storage.add_expense(
            Expense(amount=20, category="Transport",
                    description="Bus", date="2024-01-15"))
        found = self.storage.get_expense_by_id(expense.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.description, "Bus")

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.storage.get_expense_by_id(999))

    def test_delete(self):
        expense = self.storage.add_expense(
            Expense(amount=15, category="Food",
                    description="Coffee", date="2024-01-15"))
        self.assertTrue(self.storage.delete_expense(expense.id))
        self.assertEqual(len(self.storage.get_all_expenses()), 0)

    def test_delete_not_found(self):
        self.assertFalse(self.storage.delete_expense(999))

    def test_update(self):
        expense = self.storage.add_expense(
            Expense(amount=10, category="Food",
                    description="Snack", date="2024-01-15"))
        updated = self.storage.update_expense(expense.id, amount=15.0)
        self.assertEqual(updated.amount, 15.0)

        fetched = self.storage.get_expense_by_id(expense.id)
        self.assertEqual(fetched.amount, 15.0)

    def test_clear_all(self):
        self.storage.add_expense(
            Expense(amount=10, category="Food",
                    description="Test", date="2024-01-15"))
        self.storage.add_expense(
            Expense(amount=20, category="Transport",
                    description="Test", date="2024-01-15"))
        self.storage.clear_all_expenses()
        self.assertEqual(len(self.storage.get_all_expenses()), 0)

    def test_budgets(self):
        self.storage.set_budgets({"Food": 500, "Transport": 200})
        budgets = self.storage.get_budgets()
        self.assertEqual(budgets["Food"], 500)
        self.assertEqual(budgets["Transport"], 200)


class TestExpenseTracker(unittest.TestCase):
    """Tests for the ExpenseTracker business logic."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        storage = Storage(self.tmp.name)
        self.tracker = ExpenseTracker(storage)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def _add_sample_expenses(self):
        self.tracker.add_expense(50.0, "Food", "Groceries", "2024-01-10")
        self.tracker.add_expense(30.0, "Transport", "Gas", "2024-01-12")
        self.tracker.add_expense(100.0, "Food", "Dinner", "2024-01-15")

    def test_add_expense(self):
        expense = self.tracker.add_expense(
            25.0, "Food", "Lunch", "2024-01-15")
        self.assertIsNotNone(expense.id)

    def test_get_all_expenses(self):
        self._add_sample_expenses()
        expenses = self.tracker.get_all_expenses()
        self.assertEqual(len(expenses), 3)

    def test_total_spent(self):
        self._add_sample_expenses()
        self.assertEqual(self.tracker.get_total_spent(), 180.0)

    def test_category_breakdown(self):
        self._add_sample_expenses()
        breakdown = self.tracker.get_category_breakdown()
        self.assertIn("Food", breakdown)
        self.assertIn("Transport", breakdown)
        self.assertEqual(breakdown["Food"], 150.0)
        self.assertEqual(breakdown["Transport"], 30.0)

    def test_monthly_summary(self):
        self._add_sample_expenses()
        summary = self.tracker.get_monthly_summary()
        self.assertIn("2024-01", summary)
        self.assertEqual(summary["2024-01"], 180.0)

    def test_filter_by_category(self):
        self._add_sample_expenses()
        expenses = self.tracker.get_expenses_by_category("Food")
        self.assertEqual(len(expenses), 2)

    def test_filter_by_date_range(self):
        self._add_sample_expenses()
        expenses = self.tracker.get_expenses_by_date_range(
            "2024-01-10", "2024-01-12")
        self.assertEqual(len(expenses), 2)

    def test_export_csv(self):
        self._add_sample_expenses()
        csv_path = os.path.join(os.path.dirname(self.tmp.name), "test_export.csv")
        result = self.tracker.export_to_csv(csv_path)
        self.assertTrue(os.path.exists(result))
        os.unlink(result)

    def test_stats(self):
        self._add_sample_expenses()
        stats = self.tracker.get_stats()
        self.assertEqual(stats["count"], 3)
        self.assertEqual(stats["total"], 180.0)
        self.assertEqual(stats["average"], 60.0)
        self.assertEqual(stats["max"], 100.0)
        self.assertEqual(stats["min"], 30.0)

    def test_empty_stats(self):
        stats = self.tracker.get_stats()
        self.assertEqual(stats["count"], 0)
        self.assertEqual(stats["total"], 0)

    def test_set_and_get_budgets(self):
        self.tracker.set_budgets({"Food": 500, "Transport": 200})
        budgets = self.tracker.get_budgets()
        self.assertEqual(budgets["Food"], 500)

    def test_budget_progress(self):
        self._add_sample_expenses()
        self.tracker.set_budgets({"Food": 200, "Transport": 50})
        progress = self.tracker.get_budget_progress()
        food = [p for p in progress if p["category"] == "Food"][0]
        self.assertEqual(food["spent"], 150.0)
        self.assertEqual(food["budget"], 200.0)
        self.assertFalse(food["over_budget"])

        transport = [p for p in progress if p["category"] == "Transport"][0]
        self.assertFalse(transport["over_budget"])  # 30 / 50 -> 60%, not over


if __name__ == "__main__":
    unittest.main()
