"""Data models for the Personal Expense Tracker."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Expense:
    """Represents a single expense entry."""
    amount: float
    category: str
    description: str
    date: str  # YYYY-MM-DD format
    id: Optional[int] = None

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if not self.category.strip():
            raise ValueError("Category cannot be empty")
        if not self.description.strip():
            raise ValueError("Description cannot be empty")
        # Validate date format
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {self.date}. Use YYYY-MM-DD.")

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Expense":
        return Expense(
            id=data.get("id"),
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data["date"],
        )
