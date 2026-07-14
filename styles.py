"""Styles, colors, and formatting helpers for beautiful terminal output.

Uses ANSI escape codes for colors (works on Windows 10+, macOS, Linux).
No external dependencies required.
"""

import os
import shutil

# ─── ANSI Color Codes ──────────────────────────────────────────────────────

class Color:
    """Terminal color and style constants."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    # Bright foreground colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


# ─── Unicode Symbols ───────────────────────────────────────────────────────

class Icon:
    """Visual symbols/icons for the UI."""
    CHECK = "✓"
    CROSS = "✗"
    WARN = "⚠"
    STAR = "★"
    ARROW = "▸"
    BULLET = "•"
    DASH = "─"
    PIPE = "│"
    CORNER_TL = "┌"
    CORNER_TR = "┐"
    CORNER_BL = "└"
    CORNER_BR = "┘"
    H_LINE = "─"
    V_LINE = "│"
    T_DOWN = "┬"
    T_UP = "┴"
    T_RIGHT = "├"
    T_LEFT = "┤"
    CROSS_S = "┼"
    BLOCK = "█"
    HALF_BLOCK = "▓"
    DARK_SHADE = "▒"
    LIGHT_SHADE = "░"
    EMPTY = " "
    MONEY = "₹"


# ─── Terminal Detection ────────────────────────────────────────────────────

def _supports_color() -> bool:
    """Check if the terminal supports ANSI color codes."""
    # Check for common color-supporting terminals
    if os.environ.get("TERM"):
        return True
    # Windows 10+ supports ANSI via Virtual Terminal Processing
    if os.name == "nt":
        ver = os.sys.getwindowsversion() if hasattr(os, 'sys') else None
        if ver and ver.major >= 10:
            return True
        return False
    return True


def enable_windows_ansi():
    """Enable ANSI escape codes on Windows cmd.exe."""
    if os.name == "nt":
        os.system("")  # This enables VT processing on Windows 10+


# ─── Terminal Width ────────────────────────────────────────────────────────

def terminal_width() -> int:
    """Get the current terminal width, defaulting to 80."""
    return shutil.get_terminal_size((80, 20)).columns


# ─── Styling Helpers ───────────────────────────────────────────────────────

def colored(text: str, *styles: str) -> str:
    """Wrap text in ANSI style codes. Falls back to plain text if no color."""
    if not _supports_color():
        return text.strip()
    codes = "".join(styles)
    return f"{codes}{text}{Color.RESET}"


def bold(text: str) -> str:
    return colored(text, Color.BOLD)


def dim(text: str) -> str:
    return colored(text, Color.DIM)


def italic(text: str) -> str:
    return colored(text, Color.ITALIC)


def green(text: str) -> str:
    return colored(text, Color.GREEN)


def red(text: str) -> str:
    return colored(text, Color.RED)


def yellow(text: str) -> str:
    return colored(text, Color.YELLOW)


def cyan(text: str) -> str:
    return colored(text, Color.CYAN)


def blue(text: str) -> str:
    return colored(text, Color.BLUE)


def magenta(text: str) -> str:
    return colored(text, Color.MAGENTA)


def money(text: str) -> str:
    """Format money amount in bright green bold."""
    return colored(text, Color.BRIGHT_GREEN, Color.BOLD)


def danger(text: str) -> str:
    """Format danger/error text in bright red bold."""
    return colored(text, Color.BRIGHT_RED, Color.BOLD)


def success(text: str) -> str:
    return colored(f" {Icon.CHECK} {text}", Color.GREEN)


def error(text: str) -> str:
    return colored(f" {Icon.CROSS} {text}", Color.RED)


def warning(text: str) -> str:
    return colored(f" {Icon.WARN} {text}", Color.YELLOW)


def highlight(text: str) -> str:
    """Highlight text for emphasis."""
    return colored(text, Color.BRIGHT_CYAN, Color.BOLD)


def header_text(text: str) -> str:
    """Format header text in bright blue bold."""
    return colored(text, Color.BRIGHT_BLUE, Color.BOLD)


def label(text: str, width: int = 12) -> str:
    """Format a label with dim color and fixed width."""
    return colored(f"{text:<{width}}", Color.DIM)


# ─── Box Drawing ───────────────────────────────────────────────────────────

def horizontal_line(char: str = Icon.H_LINE) -> str:
    """Draw a full-width horizontal line."""
    width = min(terminal_width() - 2, 60)
    return colored(char * width, Color.DIM)


def section(title: str):
    """Print a section header with decorative lines."""
    width = min(terminal_width() - 2, 60)
    title = f"  {title}  "
    padding = width - len(title)
    left = padding // 2
    right = padding - left
    line = colored(Icon.H_LINE * left, Color.DIM)
    end = colored(Icon.H_LINE * right, Color.DIM)
    print(f"\n{line}{bold(header_text(title))}{end}")


# ─── Formatters ────────────────────────────────────────────────────────────

def fmt_money(amount: float) -> str:
    """Format amount with INR symbol."""
    return f"₹{amount:,.2f}"


def fmt_money_colored(amount: float) -> str:
    """Format amount with INR symbol and color."""
    return money(f"₹{amount:,.2f}")


def fmt_percent(pct: float) -> str:
    """Format percentage with appropriate color."""
    text = f"{pct:5.1f}%"
    if pct > 100:
        return danger(text)
    elif pct > 80:
        return yellow(text)
    return colored(text, Color.DIM)


def fmt_bar(value: float, total: float, width: int = 20) -> str:
    """Create a visual bar (e.g. for category breakdown or budget)."""
    if total <= 0:
        return dim(Icon.LIGHT_SHADE * width)
    ratio = min(value / total, 1.0)
    filled = int(ratio * width)
    empty = width - filled

    if ratio > 0.9:
        bar_color = Color.BRIGHT_RED
    elif ratio > 0.7:
        bar_color = Color.BRIGHT_YELLOW
    else:
        bar_color = Color.BRIGHT_GREEN

    filled_part = colored(Icon.BLOCK * filled, bar_color)
    empty_part = dim(Icon.LIGHT_SHADE * empty)
    return f"{filled_part}{empty_part}"
