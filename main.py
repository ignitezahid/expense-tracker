#!/usr/bin/env python3
"""Personal Expense Tracker — Beautiful Interactive CLI.

Track, categorize, and report your expenses from the terminal in style.
Created by ignitezahid.

Usage:
    python main.py
"""

import os
import sys
from datetime import datetime

from tracker import ExpenseTracker
from styles import (
    Color, Icon, enable_windows_ansi, section,
    bold, dim, green, red, yellow, cyan, blue, magenta,
    money, danger, success, error, warning, highlight,
    fmt_money, fmt_money_colored, fmt_percent, fmt_bar,
    horizontal_line, terminal_width,
)


# ─── Screen Management ─────────────────────────────────────────────────────

def clear():
    """Clear screen and show title bar."""
    os.system("cls" if os.name == "nt" else "clear")


def print_app_header():
    """Print the app title header."""
    width = min(terminal_width() - 2, 60)
    print()
    print(f"  {bold(dim(Icon.H_LINE * width))}")
    print(f"  {bold(cyan(Icon.STAR + ' PERSONAL EXPENSE TRACKER ' + Icon.STAR))}")
    print(f"  {dim('  Track your spending like a pro')}")
    print(f"  {bold(dim(Icon.H_LINE * width))}")


def print_status_bar(tracker):
    """Show a compact status bar with key metrics."""
    expenses = tracker.get_all_expenses()
    count = len(expenses)
    total = tracker.get_total_spent()
    budgets = tracker.get_budgets()

    parts = [f"{dim('Expenses:')} {bold(str(count))}"]
    parts.append(f"{dim('Total:')} {fmt_money_colored(total)}")

    if budgets:
        progress = tracker.get_budget_progress()
        total_budget = sum(b.get("budget", 0) for b in progress)
        if total_budget > 0:
            total_spent = sum(b.get("spent", 0) for b in progress)
            pct = (total_spent / total_budget) * 100
            parts.append(f"{dim('Budget:')} {fmt_percent(pct)}")

    print("  " + "  |  ".join(parts))
    print()


# ─── Input Helpers ─────────────────────────────────────────────────────────

def pause():
    """Wait for Enter with styled prompt."""
    print()
    input(f"  {dim('Press Enter to continue...')}")


def prompt(text: str, default: str = None, required: bool = False) -> str:
    """Get user input with a styled prompt."""
    if default is not None:
        full = f"  {bold(text)} [{dim(default)}]: "
    else:
        full = f"  {bold(text)}: "
    while True:
        val = input(full).strip()
        if not val and default is not None:
            return default
        if not val and required:
            print(f"  {warning('This cannot be empty.')}")
            continue
        return val


def prompt_int(text: str, min_val=None, max_val=None, default=None) -> int:
    """Get a validated integer."""
    while True:
        raw = prompt(text, default=str(default) if default else None)
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"  {warning(f'Must be at least {min_val}.')}")
                continue
            if max_val is not None and val > max_val:
                print(f"  {warning(f'Must be at most {max_val}.')}")
                continue
            return val
        except ValueError:
            print(f"  {warning('Please enter a valid number.')}")


def prompt_float(text: str, min_val=0) -> float:
    """Get a validated float."""
    while True:
        raw = prompt(text)
        try:
            val = float(raw)
            if val < min_val:
                print(f"  {warning(f'Must be at least {min_val}.')}")
                continue
            return val
        except ValueError:
            print(f"  {warning('Please enter a valid number.')}")


def prompt_date(text: str = "Date (YYYY-MM-DD)", default: str = None) -> str:
    """Get a valid date string."""
    if default is None:
        default = datetime.now().strftime("%Y-%m-%d")
    while True:
        val = prompt(text, default=default)
        if val == default:
            return val
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print(f"  {warning('Invalid format. Use YYYY-MM-DD.')}")


# ─── Table Drawing ─────────────────────────────────────────────────────────

def print_table(headers: list, rows: list, col_styles: list = None):
    """Draw a formatted table with borders, headers, and styled cells.

    All header and cell values must be PLAIN strings (no ANSI codes).
    Styling is applied AFTER width formatting for perfect alignment.

    Args:
        headers: List of plain header strings
        rows: List of lists of plain cell strings
        col_styles: Optional list of style functions per column.
                    None = no styling for that column.
    """
    num_cols = len(headers)
    if col_styles is None:
        col_styles = [None] * num_cols

    # Calculate column widths from plain text only
    col_widths = []
    for i in range(num_cols):
        w = len(str(headers[i]))
        for row in rows:
            if i < len(row):
                w = max(w, len(str(row[i])))
        col_widths.append(w + 2)  # 2 for padding spaces

    # Build separator lines
    def make_sep(left, mid, right):
        sep = left
        for i, w in enumerate(col_widths):
            sep += Icon.H_LINE * (w + 2)
            if i < num_cols - 1:
                sep += mid
            else:
                sep += right
        return sep

    sep_top = make_sep(Icon.CORNER_TL, Icon.T_DOWN, Icon.CORNER_TR)
    sep_mid = make_sep(Icon.T_RIGHT, Icon.CROSS_S, Icon.T_LEFT)
    sep_bot = make_sep(Icon.CORNER_BL, Icon.T_UP, Icon.CORNER_BR)

    # Print top border
    print(f"    {dim(sep_top)}")

    # Print header row — format plain text to width, then style
    cells = []
    for i, h in enumerate(headers):
        w = col_widths[i]
        plain = f"{str(h):>{w}}"  # format to correct width as plain text
        styled = bold(blue(plain))  # THEN apply style
        cells.append(f" {styled} ")
    print(f"    {Icon.V_LINE}" + f"{Icon.V_LINE}".join(cells) + f"{Icon.V_LINE}")

    # Print header-data separator
    print(f"    {dim(sep_mid)}")

    # Print data rows
    for row in rows:
        cells = []
        for i in range(num_cols):
            val = str(row[i]) if i < len(row) else ""
            w = col_widths[i]
            plain = f"{val:>{w}}"  # format to correct width as plain text
            style_fn = col_styles[i] if i < len(col_styles) else None
            if style_fn:
                styled = style_fn(plain)  # THEN apply style
            else:
                styled = plain
            cells.append(f" {styled} ")
        print(f"    {Icon.V_LINE}" + f"{Icon.V_LINE}".join(cells) + f"{Icon.V_LINE}")

    # Print bottom border
    print(f"    {dim(sep_bot)}")


# ─── Menu Handlers ─────────────────────────────────────────────────────────

def menu_add(tracker):
    """Interactive prompt to add an expense."""
    section("ADD EXPENSE")

    categories_str = dim(", ".join(tracker.CATEGORIES))
    print(f"  {bold('Categories:')} {categories_str}")
    print()

    category = prompt("Category").capitalize()
    if category not in tracker.CATEGORIES:
        msg = f"'{category}' added as custom category."
        print(f"  {warning(msg)}")

    amount = prompt_float(f"Amount ({Icon.MONEY})")
    description = prompt("Description", required=True)
    date = prompt_date()

    try:
        expense = tracker.add_expense(amount, category, description, date)
        print()
        print(f"  {success(f'Expense added! [ID: {expense.id}]')}")
        print_expense_row(expense, indent=4)
    except ValueError as e:
        print(f"  {error(str(e))}")

    pause()


def menu_list(tracker):
    """List expenses with optional filters."""
    expenses = tracker.get_all_expenses()
    if not expenses:
        print(f"\n  {dim('No expenses recorded yet.')} {bold('Add one first!')}")
        pause()
        return

    section("VIEW ALL EXPENSES")
    print(f"  {dim('Filters (leave blank to skip):')}")
    print()
    cat_filter = prompt("Category filter").capitalize()
    start = prompt("Start date")
    end = prompt("End date")

    if cat_filter:
        expenses = [e for e in expenses if e.category.lower() == cat_filter.lower()]
    if start:
        expenses = [e for e in expenses if e.date >= start]
    if end:
        expenses = [e for e in expenses if e.date <= end]

    if not expenses:
        print(f"\n  {warning('No expenses match your filters.')}")
        pause()
        return

    print()
    headers = ["ID", "Date", "Category", "Amount", "Description"]
    col_styles = [dim, None, cyan, money, dim]
    rows = []
    for e in expenses:
        rows.append([
            str(e.id),
            e.date,
            e.category,
            f"{Icon.MONEY}{e.amount:,.2f}",
            e.description[:30],
        ])

    print_table(headers, rows, col_styles=col_styles)

    total = sum(e.amount for e in expenses)
    print(f"\n    {bold('Total:')}  {fmt_money_colored(total)}")
    pause()


def menu_summary(tracker):
    """Show overall stats and monthly breakdown."""
    stats = tracker.get_stats()
    if stats["count"] == 0:
        print(f"\n  {dim('No expenses recorded yet.')} {bold('Add one first!')}")
        pause()
        return

    section("EXPENSE SUMMARY")

    print(f"  {dim('Total expenses:')}  {bold(str(stats['count']))}")
    total_str = fmt_money_colored(stats["total"])
    avg_str = fmt_money_colored(stats["average"])
    high_str = fmt_money_colored(stats["max"])
    low_str = fmt_money_colored(stats["min"])
    print(f"  {dim('Total spent:')}     {total_str}")
    print(f"  {dim('Average:')}         {avg_str}")
    print(f"  {dim('Highest:')}         {high_str}")
    print(f"  {dim('Lowest:')}          {low_str}")
    print(f"  {dim('Categories:')}      {bold(str(stats['categories']))}")

    print()
    section("MONTHLY BREAKDOWN")
    summary = tracker.get_monthly_summary()
    for month, total in summary.items():
        print(f"  {bold(month):<10}  {fmt_money_colored(total)}")

    if stats["total"] > 0:
        print()
        section("DAILY AVERAGE")
        first_month = list(summary.keys())[0]
        num_days = (datetime.now() - datetime.strptime(
            first_month + "-01", "%Y-%m-%d")).days
        daily_avg = stats["total"] / max(num_days, 1)
        print(f"  {dim('Per day:')}  ~{fmt_money_colored(daily_avg)}")

    pause()


def menu_categories(tracker):
    """Show spending breakdown by category with visual bars."""
    breakdown = tracker.get_category_breakdown()
    if not breakdown:
        print(f"\n  {dim('No expenses recorded yet.')}")
        pause()
        return

    total = sum(breakdown.values())
    section("CATEGORY BREAKDOWN")
    print()

    max_name_len = max(len(c) for c in breakdown)
    name_width = max(max_name_len + 1, 12)

    for category, amount in breakdown.items():
        pct = (amount / total) * 100 if total > 0 else 0
        bar = fmt_bar(amount, total)
        amt_str = fmt_money_colored(amount)
        pct_str = fmt_percent(pct)
        print(f"  {bold(category):<{name_width}} {bar}  {amt_str:>14}  {pct_str}")

    print(f"  {dim(Icon.H_LINE * (name_width + 42))}")
    print(f"  {bold('TOTAL'):<{name_width}} "
          f"{dim(Icon.LIGHT_SHADE * 20)}  "
          f"{fmt_money_colored(total):>14}  {dim('100.0%')}")
    pause()


def menu_budget(tracker):
    """Set and view budget progress."""
    section("BUDGET TRACKER")

    # Show existing budgets
    current = tracker.get_budgets()
    if current:
        print(f"\n  {bold('Current budgets:')}")
        for cat, amt in current.items():
            print(f"    {cyan(cat):<12} = {fmt_money_colored(amt)}")

    # Set new budgets
    print(f"\n  {bold('Set budgets:')}  {dim('Category=Amount (space-separated)')}")
    print(f"  {dim('Categories:')} {dim(', '.join(tracker.CATEGORIES))}")
    inp = prompt(f"e.g. {dim('Food=5000 Transport=2000')}", default="")

    if inp:
        new_budgets = {}
        for item in inp.split():
            try:
                cat, amt = item.split("=")
                new_budgets[cat.strip().capitalize()] = float(amt)
            except ValueError:
                print(f"  {warning(f'Skipping invalid: {item}')}")
        if new_budgets:
            tracker.set_budgets(new_budgets)
            print(f"  {success('Budgets saved!')}")

    # Show progress
    progress = tracker.get_budget_progress()
    if progress:
        print()
        section("BUDGET vs SPENDING")
        print()
        for item in progress:
            cat = item["category"]
            spent = item["spent"]
            budget = item["budget"]
            pct = item["percent"]
            over = item["over_budget"]

            if budget > 0:
                bar = fmt_bar(spent, budget)
                spent_str = fmt_money_colored(spent)
                budget_str = fmt_money_colored(budget)
                pct_str = fmt_percent(pct)
                status = danger("OVER!") if over else green("OK")
                print(f"  {bold(cat):<12} {bar}  "
                      f"{spent_str:>10} / {budget_str:<10}  "
                      f"{pct_str}  [{status}]")
            else:
                print(f"  {bold(cat):<12}  {dim(Icon.LIGHT_SHADE * 20)}  "
                      f"{fmt_money_colored(spent):>10}  {dim('(no budget)')}")

    pause()


def menu_export(tracker):
    """Export to CSV."""
    filename = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = tracker.export_to_csv(filename)
    print(f"\n  {success(f'Exported to: {filepath}')}")
    pause()


def print_expense_row(expense, indent: int = 2):
    """Print a single expense row — plain format first, then style."""
    pad = " " * indent
    id_str = f"[{expense.id:>4}]"
    cat_str = f"{expense.category:<15}"
    amt_str = f"{Icon.MONEY}{expense.amount:,.2f}"
    amt_padded = f"{amt_str:>12}"
    print(f"  {pad}{dim(id_str)} {expense.date}  {cyan(cat_str)} {money(amt_padded)}")
    print(f"  {pad} {dim(Icon.ARROW)} {expense.description}")


def menu_delete(tracker):
    """Delete an expense."""
    expenses = tracker.get_all_expenses()
    if not expenses:
        print(f"\n  {dim('No expenses to delete.')}")
        pause()
        return

    section("DELETE EXPENSE")
    print()
    for e in expenses[:10]:
        print_expense_row(e)
    if len(expenses) > 10:
        print(f"  {dim(f'... and {len(expenses) - 10} more')}")

    print()
    expense_id = prompt_int("Enter ID to delete", min_val=1)

    confirm = prompt(f"Delete expense [{bold(str(expense_id))}]? (yes/no)")
    if confirm.lower() != "yes":
        print(f"  {warning('Cancelled.')}")
        pause()
        return

    if tracker.delete_expense(expense_id):
        print(f"  {success(f'Expense [ID: {expense_id}] deleted!')}")
    else:
        print(f"  {error(f'Expense [ID: {expense_id}] not found.')}")
    pause()


def menu_edit(tracker):
    """Edit an expense."""
    expenses = tracker.get_all_expenses()
    if not expenses:
        print(f"\n  {dim('No expenses to edit.')}")
        pause()
        return

    section("EDIT EXPENSE")
    print()
    for e in expenses[:10]:
        print_expense_row(e)
    if len(expenses) > 10:
        print(f"  {dim(f'... and {len(expenses) - 10} more')}")

    print()
    expense_id = prompt_int("Enter ID to edit", min_val=1)
    expense = tracker.get_expense(expense_id)
    if not expense:
        print(f"  {error(f'Expense [ID: {expense_id}] not found.')}")
        pause()
        return

    print(f"\n  {bold('Editing')} {dim(f'[ID: {expense_id}]')}")
    print(f"  {dim('Leave blank to keep current value.')}")
    print()

    kwargs = {}

    amt = prompt(f"Amount ({Icon.MONEY})", default=str(expense.amount))
    if amt != str(expense.amount):
        kwargs["amount"] = float(amt)

    cat = prompt("Category", default=expense.category)
    if cat != expense.category:
        kwargs["category"] = cat.capitalize()

    desc = prompt("Description", default=expense.description)
    if desc != expense.description:
        kwargs["description"] = desc

    date = prompt_date(default=expense.date)
    if date != expense.date:
        kwargs["date"] = date

    if kwargs:
        result = tracker.update_expense(expense_id, **kwargs)
        if result:
            print(f"\n  {success(f'Expense [ID: {expense_id}] updated!')}")
            print_expense_row(result, indent=2)
    else:
        print(f"\n  {yellow('No changes made.')}")

    pause()


def menu_clear(tracker):
    """Clear all expenses with confirmation."""
    count = len(tracker.get_all_expenses())
    if count == 0:
        print(f"\n  {dim('No expenses to clear.')}")
        pause()
        return

    section("CLEAR ALL EXPENSES")
    print(f"\n  {danger('⚠  DANGER ZONE')}")
    print(f"  {warning(f'This will PERMANENTLY delete all {bold(str(count))} expenses!')}")
    print()

    confirm = prompt("Type 'yes' to confirm")
    if confirm.lower() == "yes":
        tracker.storage.clear_all_expenses()
        print(f"\n  {success(f'All {count} expenses cleared.')}")
    else:
        print(f"\n  {warning('Cancelled.')}")
    pause()


# ─── Main Menu ─────────────────────────────────────────────────────────────

def print_menu():
    """Print the main menu and return the user's choice."""
    # The content area between V_LINE chars is 56 chars wide.
    # With 2-space indent + V_LINE + space, the total line is 59 chars.
    inner_width = 56
    left_pad = "  "
    left_border = f"{left_pad}{Icon.V_LINE} "  # "  │ "
    right_border = Icon.V_LINE

    def print_menu_line(plain_text: str, styled_text: str):
        """Print a menu line with correct padding.
        plain_text is used for length calculation (no ANSI codes).
        styled_text is used for display (with ANSI codes).
        """
        padding = inner_width - len(plain_text) - 1  # -1 for space after left_border
        print(f"{left_border}{styled_text}{' ' * padding}{right_border}")

    def print_border(left, right):
        """Print a horizontal border line."""
        line = left + Icon.H_LINE * inner_width + right
        print(f"{left_pad}{bold(dim(line))}")

    # Top border
    print_border(Icon.CORNER_TL, Icon.CORNER_TR)

    # Menu items
    items = [
        (1, Icon.BULLET, "Add Expense"),
        (2, Icon.BULLET, "View All Expenses"),
        (3, Icon.BULLET, "View Summary & Stats"),
        (4, Icon.BULLET, "Category Breakdown"),
        (5, Icon.BULLET, "Set & View Budgets"),
        (6, Icon.BULLET, "Export to CSV"),
        (7, Icon.BULLET, "Delete Expense"),
        (8, Icon.BULLET, "Edit Expense"),
        (9, Icon.BULLET, "Clear All Expenses"),
    ]

    for num, icon, label in items:
        plain = f"{icon}  {num}.  {label}"
        styled = f"{bold(icon)}  {bold(str(num))}.  {label}"
        print_menu_line(plain, styled)

    # Separator
    print_border(Icon.T_RIGHT, Icon.T_LEFT)

    # Exit item
    plain_exit = f"{Icon.EMPTY}  0.  Exit"
    styled_exit = f"{bold(Icon.EMPTY)}  {bold('0')}.  Exit"
    print_menu_line(plain_exit, styled_exit)

    # Bottom border
    print_border(Icon.CORNER_BL, Icon.CORNER_BR)

    print()
    return prompt_int("Your choice", min_val=0, max_val=9)


def main():
    """Main interactive loop."""
    enable_windows_ansi()
    tracker = ExpenseTracker()
    total_expenses = len(tracker.get_all_expenses())
    first_run = total_expenses == 0

    while True:
        clear()
        print_app_header()

        if first_run:
            print(f"  {green('Welcome!')} {dim('Start by adding your first expense.')}")
            first_run = False

        print_status_bar(tracker)
        choice = print_menu()

        if choice == 0:
            clear()
            print_app_header()
            print()
            print(f"  {bold('Goodbye!')} {dim('Tracked')} {bold(str(total_expenses))} "
                  f"{dim('expense(s).')}")
            print(f"  {dim('Total spent:')} {fmt_money_colored(tracker.get_total_spent())}")
            print(f"  {dim('Built by')} {bold('ignitezahid')} {dim(Icon.STAR)}")
            print()
            break
        elif choice == 1:
            menu_add(tracker)
        elif choice == 2:
            menu_list(tracker)
        elif choice == 3:
            menu_summary(tracker)
        elif choice == 4:
            menu_categories(tracker)
        elif choice == 5:
            menu_budget(tracker)
        elif choice == 6:
            menu_export(tracker)
        elif choice == 7:
            menu_delete(tracker)
        elif choice == 8:
            menu_edit(tracker)
        elif choice == 9:
            menu_clear(tracker)

        total_expenses = len(tracker.get_all_expenses())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(f"\n  {bold('Goodbye!')}\n")
        sys.exit(0)
