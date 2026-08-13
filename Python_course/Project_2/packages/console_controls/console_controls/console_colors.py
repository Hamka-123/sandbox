"""
console_colors.py
=================
Utility module for printing colored text in the console.

Usage:
    from console_colors import colorized_print, colorized_input, colorized_exception
"""

# ===== ANSI escape sequences for colors =====
COLORS = {
    'BLACK'   : "\033[30m",
    'RED'     : "\033[31m",
    'GREEN'   : "\033[32m",
    'YELLOW'  : "\033[33m",
    'BLUE'    : "\033[34m",
    'MAGENTA' : "\033[35m",
    'CYAN'    : "\033[36m",
    'WHITE'   : "\033[37m",
    'RESET'   : "\033[0m"
}
BG_COLORS = {
    'BLACK'   : "\033[40m",
    'RED'     : "\033[41m",
    'GREEN'   : "\033[42m",
    'YELLOW'  : "\033[43m",
    'BLUE'    : "\033[44m",
    'MAGENTA' : "\033[45m",
    'CYAN'    : "\033[46m",
    'WHITE'   : "\033[47m"
}
DEFAULT_COLOR_TEXT = "BLUE"
DEFAULT_COLOR_ERROR = "RED"

# ===== Validation =====
def validate_color_param(color: str = None, bg_color: str = None):
    """Validate foreground and background color names."""
    if color is not None and color.upper() not in COLORS.keys():
        raise ValueError(f"Invalid foreground color: {color}. Available: {list(COLORS.keys())}")
    if bg_color is not None and bg_color.upper() not in BG_COLORS.keys():
        raise ValueError(f"Invalid background color: {bg_color}. Available: {list(BG_COLORS.keys())}")

# ===== Core functions =====
def get_color_code(color:str) -> str:
    """Return ANSI escape code for a color name."""
    validate_color_param(color=color)
    return COLORS.get(color.upper(), COLORS['RESET'])

def set_color(text:str, color:str = DEFAULT_COLOR_TEXT) -> str:
    """Wrap text in the given color with automatic reset."""
    validate_color_param(color=color)
    return f"{get_color_code(color)}{text}{COLORS['RESET']}"

def set_bg_color(text: str, bg_color: str, color: str = DEFAULT_COLOR_TEXT) -> str:
    """Wrap text in foreground and background colors with automatic reset."""
    validate_color_param(color=color, bg_color=bg_color)
    fg_code = COLORS.get(color.upper(), COLORS['RESET'])
    bg_code = BG_COLORS.get(bg_color.upper(), "")
    return f"{fg_code}{bg_code}{text}{COLORS['RESET']}"
    
def reset_color(text:str) -> str:
    """Append reset code to text (useful if text already contains ANSI codes)."""
    return f"{text}{COLORS['RESET']}"

# ===== Convenience functions =====

def colorized_print(text: str, color: str = DEFAULT_COLOR_TEXT, bg_color: str = None) -> None:
    """Print text with optional foreground and background color."""
    if bg_color:
        print(set_bg_color(text, bg_color, color))
    else:
        print(set_color(text, color))
    
def colorized_input(prompt: str, color: str = DEFAULT_COLOR_TEXT, bg_color: str = None) -> str:
    """Prompt input with optional foreground and background color."""
    if bg_color:
        colored_prompt = set_bg_color(prompt, bg_color, color)
    else:
        colored_prompt = set_color(prompt, color)
    return input(colored_prompt)

def colorized_exception(error: Exception, color: str = DEFAULT_COLOR_ERROR) -> None:
    """Print exception message in color."""
    print(set_color(f"Error: {error}", color))


