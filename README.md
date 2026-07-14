<div align="center">

# 💰 Personal Expense Tracker

**A beautiful, interactive terminal app to track your spending — built entirely with Python's standard library.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](requirements.txt)

</div>

---

## ✨ Features

| Feature | What it does |
|---------|-------------|
| **➕ Add Expense** | Log spending with amount, category, description & date |
| **📋 View All** | List expenses, filter by category or date range |
| **📊 Summary & Stats** | Total, average, highest/lowest, monthly breakdown |
| **📂 Category Breakdown** | Visual bar chart of where your money goes |
| **💰 Budget Tracking** | Set per-category budgets & see real-time progress |
| **✏️ Edit / Delete** | Update or remove any expense by ID |
| **📤 Export CSV** | Download all data for Excel / analysis |
| **🎨 Colored UI** | ANSI-colored output with tables, bars & icons |
| **₹ INR Support** | Indian Rupee formatting throughout |

---

## 🚀 Quick Start

```bash
# Zero dependencies — just Python!
cd personal-expense-tracker
python main.py
```

That's it! The interactive menu will open:

```
  ┌────────────────────────────────────────────────────────────┐
  │  ★  PERSONAL EXPENSE TRACKER  ★                           │
  │    Track your spending like a pro                         │
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

Just type the number and press **Enter** to navigate.

---

## 📖 Walkthrough

### Adding an expense
```
  >> 1  (Add Expense)

  ────  ADD EXPENSE  ────
  Categories: Food, Transport, Housing, ...

  Category: Food
  Amount (₹): 450
  Description: Lunch with friends
  Date (YYYY-MM-DD) [2026-07-14]:

  ✓ Expense added! [ID: 1]
    [   1] 2026-07-14  Food             ₹450.00
     ▸ Lunch with friends
```

### Viewing your stats
```
  >> 3  (View Summary & Stats)

  ────  EXPENSE SUMMARY  ────
  Total expenses:  12
  Total spent:     ₹45,230.00
  Average:         ₹3,769.17
  Highest:         ₹12,000.00
  Lowest:          ₹50.00
  Categories:      5

  ────  MONTHLY BREAKDOWN  ────
  July 2026       ₹21,500.00
  June 2026       ₹15,730.00
  ...
```

### Category breakdown
```
  >> 4  (Category Breakdown)

  ────  CATEGORY BREAKDOWN  ────
  Food         ████████████████░░░░  ₹15,500.00   34.3%
  Transport    █████████░░░░░░░░░░░  ₹8,400.00    18.6%
  Shopping     ███████░░░░░░░░░░░░  ₹6,200.00    13.7%
  ...
  ────────────────────────────────────────────────
  TOTAL        ░░░░░░░░░░░░░░░░░░░░  ₹45,230.00  100.0%
```

### Budget tracking
```
  >> 5  (Set & View Budgets)

  ────  BUDGET TRACKER  ────
  Current budgets:
    Food        = ₹10,000.00
    Transport   = ₹5,000.00

  ────  BUDGET vs SPENDING  ────
  Food         ████████████████████  ₹15,500.00 / ₹10,000.00  155.0%  [OVER!]
  Transport    █████████████████░░░  ₹5,200.00  / ₹5,000.00   104.0%  [OVER!]
  Shopping     ░░░░░░░░░░░░░░░░░░░░  ₹6,200.00                       (no budget)
```

---

## 🏗 Project Structure

```
personal-expense-tracker/
├── main.py              # Interactive menu loop (run this!)
├── tracker.py           # Business logic & reporting
├── storage.py           # JSON file persistence
├── models.py            # Expense data model
├── styles.py            # ANSI colors, icons, table drawing
├── requirements.txt     # Dependencies (stdlib only!)
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── tests/
    ├── __init__.py
    ├── conftest.py      # Test fixtures
    └── test_tracker.py  # 26 unit tests
```

---

## 🧪 Running Tests

```bash
python -m unittest tests/test_tracker.py -v
```

Expected output: **26 tests passed** ✅

---

## 📦 Building as .exe

Want a standalone `.exe`? No Python installation needed!

```bash
pip install pyinstaller
pyinstaller --onefile --name expense-tracker main.py
# Your .exe is in the dist/ folder!
```

---

## 🗺 Roadmap Ideas

- [ ] 📈 Spending trend charts
- [ ] 🔄 Recurring expense detection
- [ ] 📱 Export to Google Sheets
- [ ] 🌐 Web dashboard (Flask)
- [ ] 💳 Multi-account support

---

## 📄 License

**MIT** — Free to use, modify, and share. Go build something awesome!

---

<div align="center">
  <sub>Made with ❤️ and Python's standard library</sub>
</div>
