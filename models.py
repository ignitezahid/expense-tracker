"""Data models."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Expense:
    amount: float
    category: str
    description: str
    date: str  # YYYY-MM-DD
    id: int | None = None

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
