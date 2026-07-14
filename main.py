"""Personal Expense Tracker - interactive CLI.
Created by ignitezahid."""
import os
import sys
from datetime import datetime

from tracker import ExpenseTracker
from styles import (
    enable_ansi, section,
    bold, dim, green, red, yellow, cyan, blue,
    money, danger, success, error, warning,
    fmt_money, fmt_money_c, fmt_pct, fmt_bar,
    term_width, ICO_HLINE, ICO_VLINE, ICO_STAR,
    ICO_BULLET, ICO_ARROW, ICO_MONEY, ICO_SHADE,
    ICO_TL, ICO_TR, ICO_BL, ICO_BR,
    ICO_TD, ICO_TU, ICO_TRT, ICO_TLT, ICO_CRS,
)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    w = min(term_width() - 2, 60)
    print()
    print(f"  {bold(dim(ICO_HLINE * w))}")
    print(f"  {bold(cyan(ICO_STAR + ' PERSONAL EXPENSE TRACKER ' + ICO_STAR))}")
    print(f"  {dim('  Track your spending like a pro')}")
    print(f"  {bold(dim(ICO_HLINE * w))}")


def status_bar(tracker):
    expenses = tracker.get_all_expenses()
    count = len(expenses)
    total = tracker.get_total_spent()
    budgets = tracker.get_budgets()

    parts = [f"{dim('Expenses:')} {bold(str(count))}"]
    parts.append(f"{dim('Total:')} {fmt_money_c(total)}")

    if budgets:
        progress = tracker.get_budget_progress()
        total_budget = sum(b.get("budget", 0) for b in progress)
        if total_budget > 0:
            ts = sum(b.get("spent", 0) for b in progress)
            pct = (ts / total_budget) * 100
            parts.append(f"{dim('Budget:')} {fmt_pct(pct)}")

    print("  " + "  |  ".join(parts))
    print()


def pause():
    print()
    input(f"  {dim('Press Enter to continue...')}")


def prompt(text, default=None, required=False):
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


def prompt_int(text, min_val=None, max_val=None, default=None):
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


def prompt_float(text, min_val=0):
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


def prompt_date(text="Date (YYYY-MM-DD)", default=None):
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


def print_table(headers, rows, col_styles=None):
    n = len(headers)
    if col_styles is None:
        col_styles = [None] * n

    widths = []
    for i in range(n):
        w = len(str(headers[i]))
        for row in rows:
            if i < len(row):
                w = max(w, len(str(row[i])))
        widths.append(w + 2)

    def make_sep(l, m, r):
        s = l
        for i, w in enumerate(widths):
            s += ICO_HLINE * (w + 2)
            s += m if i < n - 1 else r
        return s

    st = make_sep(ICO_TL, ICO_TD, ICO_TR)
    sm = make_sep(ICO_TRT, ICO_CRS, ICO_TLT)
    sb = make_sep(ICO_BL, ICO_TU, ICO_BR)

    print(f"    {dim(st)}")

    cells = []
    for i, h in enumerate(headers):
        w = widths[i]
        plain = f"{str(h):>{w}}"
        cells.append(f" {bold(blue(plain))} ")
    print(f"    {ICO_VLINE}" + f"{ICO_VLINE}".join(cells) + f"{ICO_VLINE}")

    print(f"    {dim(sm)}")

    for row in rows:
        cells = []
        for i in range(n):
            val = str(row[i]) if i < len(row) else ""
            w = widths[i]
            plain = f"{val:>{w}}"
            fn = col_styles[i] if i < len(col_styles) else None
            cells.append(f" {fn(plain) if fn else plain} ")
        print(f"    {ICO_VLINE}" + f"{ICO_VLINE}".join(cells) + f"{ICO_VLINE}")

    print(f"    {dim(sb)}")


def menu_add(tracker):
    section("ADD EXPENSE")
    cats = dim(", ".join(tracker.CATEGORIES))
    print(f"  {bold('Categories:')} {cats}")
    print()

    category = prompt("Category").capitalize()
    if category not in tracker.CATEGORIES:
        msg = f"'{category}' added as custom."
        print(f"  {warning(msg)}")

    amount = prompt_float(f"Amount ({ICO_MONEY})")
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
    expenses = tracker.get_all_expenses()
    if not expenses:
        print(f"\n  {dim('No expenses yet.')} {bold('Add one first!')}")
        pause()
        return

    section("VIEW ALL EXPENSES")
    print(f"  {dim('Filters (leave blank to skip):')}\n")
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
        rows.append([str(e.id), e.date, e.category,
                     f"{ICO_MONEY}{e.amount:,.2f}", e.description[:30]])

    print_table(headers, rows, col_styles=col_styles)
    total = sum(e.amount for e in expenses)
    print(f"\n    {bold('Total:')}  {fmt_money_c(total)}")
    pause()


def menu_summary(tracker):
    stats = tracker.get_stats()
    if stats["count"] == 0:
        print(f"\n  {dim('No expenses yet.')} {bold('Add one first!')}")
        pause()
        return

    section("EXPENSE SUMMARY")
    print(f"  {dim('Total expenses:')}  {bold(str(stats['count']))}")
    print(f"  {dim('Total spent:')}     {fmt_money_c(stats['total'])}")
    print(f"  {dim('Average:')}         {fmt_money_c(stats['average'])}")
    print(f"  {dim('Highest:')}         {fmt_money_c(stats['max'])}")
    print(f"  {dim('Lowest:')}          {fmt_money_c(stats['min'])}")
    print(f"  {dim('Categories:')}      {bold(str(stats['categories']))}")

    print()
    section("MONTHLY BREAKDOWN")
    for month, total in tracker.get_monthly_summary().items():
        print(f"  {bold(month):<10}  {fmt_money_c(total)}")

    if stats["total"] > 0:
        print()
        section("DAILY AVERAGE")
        first = list(tracker.get_monthly_summary().keys())[0]
        days = (datetime.now() - datetime.strptime(first + "-01", "%Y-%m-%d")).days
        avg = stats["total"] / max(days, 1)
        print(f"  {dim('Per day:')}  ~{fmt_money_c(avg)}")
    pause()


def menu_categories(tracker):
    breakdown = tracker.get_category_breakdown()
    if not breakdown:
        print(f"\n  {dim('No expenses yet.')}")
        pause()
        return

    total = sum(breakdown.values())
    section("CATEGORY BREAKDOWN")
    print()

    mw = max(max(len(c) for c in breakdown) + 1, 12)
    for cat, amt in breakdown.items():
        pct = (amt / total) * 100 if total > 0 else 0
        print(f"  {bold(cat):<{mw}} {fmt_bar(amt, total)}  {fmt_money_c(amt):>14}  {fmt_pct(pct)}")

    print(f"  {dim(ICO_HLINE * (mw + 42))}")
    print(f"  {bold('TOTAL'):<{mw}} {dim(ICO_SHADE * 20)}  {fmt_money_c(total):>14}  {dim('100.0%')}")
    pause()


def menu_budget(tracker):
    section("BUDGET TRACKER")

    current = tracker.get_budgets()
    if current:
        print(f"\n  {bold('Current budgets:')}")
        for cat, amt in current.items():
            print(f"    {cyan(cat):<12} = {fmt_money_c(amt)}")

    print(f"\n  {bold('Set budgets:')}  {dim('Category=Amount (space-separated)')}")
    print(f"  {dim('Categories:')} {dim(', '.join(tracker.CATEGORIES))}")
    inp = prompt(f"e.g. {dim('Food=5000 Transport=2000')}", default="")

    if inp:
        new = {}
        for item in inp.split():
            try:
                cat, amt = item.split("=")
                new[cat.strip().capitalize()] = float(amt)
            except ValueError:
                print(f"  {warning(f'Skipping: {item}')}")
        if new:
            tracker.set_budgets(new)
            print(f"  {success('Budgets saved!')}")

    progress = tracker.get_budget_progress()
    if progress:
        print()
        section("BUDGET vs SPENDING")
        print()
        for item in progress:
            cat = item["category"]
            sp = item["spent"]
            bud = item["budget"]
            pct = item["percent"]
            over = item["over_budget"]

            if bud > 0:
                bar = fmt_bar(sp, bud)
                sp_str = fmt_money_c(sp)
                bud_str = fmt_money_c(bud)
                pct_str = fmt_pct(pct)
                st = danger("OVER!") if over else green("OK")
                print(f"  {bold(cat):<12} {bar}  {sp_str:>10} / {bud_str:<10}  {pct_str}  [{st}]")
            else:
                print(f"  {bold(cat):<12}  {dim(ICO_SHADE * 20)}  {fmt_money_c(sp):>10}  {dim('(no budget)')}")
    pause()


def menu_export(tracker):
    fn = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fp = tracker.export_to_csv(fn)
    print(f"\n  {success(f'Exported to: {fp}')}")
    pause()


def print_expense_row(expense, indent=2):
    pad = " " * indent
    id_fmt = f"[{expense.id:>4}]"
    cat_fmt = f"{expense.category:<15}"
    amt_fmt = f"{ICO_MONEY}{expense.amount:,.2f}"
    amt_str = f"{amt_fmt:>12}"
    print(f"  {pad}{dim(id_fmt)} {expense.date}  {cyan(cat_fmt)} {money(amt_str)}")
    print(f"  {pad} {dim(ICO_ARROW)} {expense.description}")


def menu_delete(tracker):
    expenses = tracker.get_all_expenses()
    if not expenses:
        print(f"\n  {dim('Nothing to delete.')}")
        pause()
        return

    section("DELETE EXPENSE")
    print()
    for e in expenses[:10]:
        print_expense_row(e)
    if len(expenses) > 10:
        print(f"  {dim(f'... and {len(expenses) - 10} more')}")

    print()
    eid = prompt_int("Enter ID to delete", min_val=1)
    confirm = prompt(f"Delete expense [{bold(str(eid))}]? (yes/no)")
    if confirm.lower() != "yes":
        print(f"  {warning('Cancelled.')}")
        pause()
        return

    if tracker.delete_expense(eid):
        print(f"  {success(f'Expense [ID: {eid}] deleted!')}")
    else:
        print(f"  {error(f'Expense [ID: {eid}] not found.')}")
    pause()


def menu_edit(tracker):
    expenses = tracker.get_all_expenses()
    if not expenses:
        print(f"\n  {dim('Nothing to edit.')}")
        pause()
        return

    section("EDIT EXPENSE")
    print()
    for e in expenses[:10]:
        print_expense_row(e)
    if len(expenses) > 10:
        print(f"  {dim(f'... and {len(expenses) - 10} more')}")

    print()
    eid = prompt_int("Enter ID to edit", min_val=1)
    expense = tracker.get_expense(eid)
    if not expense:
        print(f"  {error(f'Expense [ID: {eid}] not found.')}")
        pause()
        return

    print(f"\n  {bold('Editing')} {dim(f'[ID: {eid}]')}")
    print(f"  {dim('Leave blank to keep current value.')}\n")

    kwargs = {}
    amt = prompt(f"Amount ({ICO_MONEY})", default=str(expense.amount))
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
        result = tracker.update_expense(eid, **kwargs)
        if result:
            print(f"\n  {success(f'Expense [ID: {eid}] updated!')}")
            print_expense_row(result, indent=2)
    else:
        print(f"\n  {yellow('No changes made.')}")
    pause()


def menu_clear(tracker):
    count = len(tracker.get_all_expenses())
    if count == 0:
        print(f"\n  {dim('Nothing to clear.')}")
        pause()
        return

    section("CLEAR ALL EXPENSES")
    print(f"\n  {danger('DANGER ZONE')}")
    print(f"  {warning(f'This will delete all {bold(str(count))} expenses!')}\n")

    confirm = prompt("Type 'yes' to confirm")
    if confirm.lower() == "yes":
        tracker.storage.clear_all_expenses()
        print(f"\n  {success(f'All {count} expenses cleared.')}")
    else:
        print(f"\n  {warning('Cancelled.')}")
    pause()


def print_menu():
    iw = 56
    lp = "  "
    lb = f"{lp}{ICO_VLINE} "
    rb = ICO_VLINE

    def pline(plain, styled):
        pad = iw - len(plain) - 1
        print(f"{lb}{styled}{' ' * pad}{rb}")

    def pbrd(l, r):
        print(f"{lp}{bold(dim(l + ICO_HLINE * iw + r))}")

    pbrd(ICO_TL, ICO_TR)

    items = [
        (1, "Add Expense"), (2, "View All Expenses"),
        (3, "View Summary & Stats"), (4, "Category Breakdown"),
        (5, "Set & View Budgets"), (6, "Export to CSV"),
        (7, "Delete Expense"), (8, "Edit Expense"),
        (9, "Clear All Expenses"),
    ]
    for num, label in items:
        plain = f"{ICO_BULLET}  {num}.  {label}"
        styled = f"{bold(ICO_BULLET)}  {bold(str(num))}.  {label}"
        pline(plain, styled)

    pbrd(ICO_TRT, ICO_TLT)

    pe = f"  0.  Exit"
    se = f"  {bold('0')}.  Exit"
    pline(pe, se)

    pbrd(ICO_BL, ICO_BR)

    print()
    return prompt_int("Your choice", min_val=0, max_val=9)


def main():
    enable_ansi()
    tracker = ExpenseTracker()
    te = len(tracker.get_all_expenses())
    first = te == 0

    while True:
        clear()
        header()
        if first:
            print(f"  {green('Welcome!')} {dim('Start by adding your first expense.')}")
            first = False
        status_bar(tracker)
        choice = print_menu()

        if choice == 0:
            clear()
            header()
            print()
            print(f"  {bold('Goodbye!')} {dim('Tracked')} {bold(str(te))} {dim('expense(s).')}")
            print(f"  {dim('Total spent:')} {fmt_money_c(tracker.get_total_spent())}")
            print(f"  {dim('Built by')} {bold('ignitezahid')} {dim(ICO_STAR)}")
            print()
            break
        elif choice == 1: menu_add(tracker)
        elif choice == 2: menu_list(tracker)
        elif choice == 3: menu_summary(tracker)
        elif choice == 4: menu_categories(tracker)
        elif choice == 5: menu_budget(tracker)
        elif choice == 6: menu_export(tracker)
        elif choice == 7: menu_delete(tracker)
        elif choice == 8: menu_edit(tracker)
        elif choice == 9: menu_clear(tracker)

        te = len(tracker.get_all_expenses())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n  {bold('Goodbye!')}\n")
        sys.exit(0)
