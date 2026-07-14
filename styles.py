"""Colors and formatting helpers for terminal output."""
import os
import shutil

# ANSI codes - just what we need
BOLD = "\033[1m"
DIM = "\033[2m"
RST = "\033[0m"
GRN = "\033[32m"
RED = "\033[31m"
YLW = "\033[33m"
CYN = "\033[36m"
BLU = "\033[34m"
MG = "\033[35m"
BGRN = "\033[92m"
BRED = "\033[91m"
BYLW = "\033[93m"

# Icons we actually use
ICO_CHECK = "✓"
ICO_CROSS = "✗"
ICO_WARN = "⚠"
ICO_STAR = "★"
ICO_BULLET = "•"
ICO_ARROW = "▸"
ICO_MONEY = "₹"
ICO_BLOCK = "█"
ICO_SHADE = "░"
ICO_HLINE = "─"
ICO_VLINE = "│"
ICO_TL = "┌"
ICO_TR = "┐"
ICO_BL = "└"
ICO_BR = "┘"
ICO_TD = "┬"
ICO_TU = "┴"
ICO_TRT = "├"
ICO_TLT = "┤"
ICO_CRS = "┼"


def _color_supported():
    if os.environ.get("TERM"):
        return True
    if os.name == "nt":
        ver = os.sys.getwindowsversion() if hasattr(os, 'sys') else None
        if ver and ver.major >= 10:
            return True
        return False
    return True


def enable_ansi():
    """Enable ANSI on Windows cmd."""
    if os.name == "nt":
        os.system("")


def term_width():
    return shutil.get_terminal_size((80, 20)).columns


def c(text, *styles):
    if not _color_supported():
        return text.strip()
    return f"{''.join(styles)}{text}{RST}"


def bold(t): return c(t, BOLD)
def dim(t): return c(t, DIM)
def green(t): return c(t, GRN)
def red(t): return c(t, RED)
def yellow(t): return c(t, YLW)
def cyan(t): return c(t, CYN)
def blue(t): return c(t, BLU)

def money(t):
    return c(t, BGRN, BOLD)

def danger(t):
    return c(t, BRED, BOLD)

def success(t):
    return c(f" {ICO_CHECK} {t}", GRN)

def error(t):
    return c(f" {ICO_CROSS} {t}", RED)

def warning(t):
    return c(f" {ICO_WARN} {t}", YLW)


def section(title):
    w = min(term_width() - 2, 60)
    t = f"  {title}  "
    pad = w - len(t)
    l = pad // 2
    r = pad - l
    print(f"\n{c(ICO_HLINE * l, DIM)}{c(t, BOLD, BLU, BOLD)}{c(ICO_HLINE * r, DIM)}")


def fmt_money(amount):
    return f"₹{amount:,.2f}"

def fmt_money_c(amount):
    return money(f"₹{amount:,.2f}")

def fmt_pct(pct):
    t = f"{pct:5.1f}%"
    if pct > 100:
        return danger(t)
    elif pct > 80:
        return yellow(t)
    return c(t, DIM)

def fmt_bar(val, total, width=20):
    if total <= 0:
        return dim(ICO_SHADE * width)
    r = min(val / total, 1.0)
    filled = int(r * width)
    empty = width - filled

    if r > 0.9:
        clr = BRED
    elif r > 0.7:
        clr = BYLW
    else:
        clr = BGRN

    return f"{c(ICO_BLOCK * filled, clr)}{dim(ICO_SHADE * empty)}"
