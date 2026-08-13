# converter_config.py

import pathlib

ROOT_PATH = pathlib.Path(__file__).parent
OFF_LINE_DATA_FILE_PATH = ROOT_PATH.joinpath("rates_data").joinpath("rates.json")
HISTORY_LOG_FILE_PATH = ROOT_PATH.joinpath("Logs").joinpath("logs.csv")

URL = "https://v6.exchangerate-api.com/v6/87a0c5a68ec687d8632a8047/latest/USD"

LOG_FILE_HEADER = ("Date","Time","From","Rate from", "To","Rate to", "Amount", "Total converted", "Connetion mode")
MAX_FILE_SIZE = 1000

MAIN_MENU = '''Select:
0 - Exit
1 - Convert currencies
2 - Create/Update local data
3 - TBD
4 - TBD
: '''

CLEAR_SCREEN = "\033[2J\033[H"
COLORS = {
    "reset": "\033[0m",      # Reset to default
    "info": "\033[32m",      # Green
    "error": "\033[31m",     # Red
    "warning": "\033[33m",   # Yellow
    "debug": "\033[36m",     # Cyan
    "success": "\033[34m",   # Blue
    "highlight": "\033[35m", # Magenta
    "white": "\033[37m",     # White
    "black": "\033[30m",     # Black
}