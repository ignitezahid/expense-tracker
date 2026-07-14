# Personal Expense Tracker

Track your spending from the terminal. Built with Python's standard library, no pip install needed.

## Features

- Add expenses with category, amount, description and date
- View all expenses, filter by category or date range
- Monthly summary with totals, averages, highs and lows
- Category breakdown with visual bars
- Budget tracking - set limits per category, see if you're over
- Edit or delete expenses
- Export to CSV
- Colored terminal UI with INR formatting

## Quick start

```
cd personal-expense-tracker
python main.py
```

You'll see a menu:

```
  ┌────────────────────────────────────────────────────────────┐
  │  ★  PERSONAL EXPENSE TRACKER  ★                           │
  ├────────────────────────────────────────────────────────────┤
  │  •  1.  Add Expense                                       │
  │  •  2.  View All Expenses                                 │
  │  •  3.  View Summary & Stats                              │
  │  •  4.  Category Breakdown                                │
  │  •  5.  Set & View Budgets                                │
  │  •  6.  Export to CSV                                     │
  │  •  7.  Delete Expense                                    │
  │  •  8.  Edit Expense                                      │
  │  •  9.  Clear All Expenses                                │
  ├────────────────────────────────────────────────────────────┤
  │    0.  Exit                                               │
  └────────────────────────────────────────────────────────────┘
```

Just pick a number and hit enter.

## Walkthrough

**Add an expense:**
```
  >> 1

  Category: Food
  Amount (₹): 450
  Description: Lunch with friends
  Date: 2026-07-14

  ✓ Expense added! [ID: 1]
    [   1] 2026-07-14  Food             ₹450.00
     ▸ Lunch with friends
```

**Check your stats:**
```
  >> 3

  Total expenses:  12
  Total spent:     ₹45,230.00
  Average:         ₹3,769.17
  Highest:         ₹12,000.00
  Lowest:          ₹50.00
```

**Category breakdown:**
```
  >> 4

  Food         ████████████████░░░░  ₹15,500.00   34.3%
  Transport    █████████░░░░░░░░░░░  ₹8,400.00    18.6%
  TOTAL        ░░░░░░░░░░░░░░░░░░░░  ₹45,230.00  100.0%
```

## Project structure

```
personal-expense-tracker/
├── main.py        # Menu loop
├── tracker.py     # Business logic
├── storage.py     # JSON persistence
├── models.py      # Data model
├── styles.py      # Colors and formatting
├── LICENSE
├── README.md
└── tests/
    └── test_tracker.py
```

## Running tests

```
python -m unittest tests/test_tracker.py -v
```

## Building an .exe

```
pip install pyinstaller
pyinstaller --onefile --name expense-tracker main.py
```

## License

MIT
