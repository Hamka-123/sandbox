# currency_hub.py

"""
A simple currency conversion tool that provides online and offline currency conversion services.

Features:
- Converts an amount from one currency to another using up-to-date rates (via `conversion`).
- Clears the console screen for better user experience (via `clear_screen`).
- Displays a user-friendly menu (via `show_menu`).
- Fetches currency rates from an online API if available (handled by `fetch_data` from update_from_online module).
- Stores rates locally in a JSON file for offline use.
- Prompts the user to update local rates if the file already exists.
- Logs each conversion operation with date, time, source/target currencies, 
  amount, converted amount, and connection mode (online/offline).
- Provides clear and user-friendly messages for errors, warnings, and confirmations.

Dependencies:
- update_from_online.py (imports `fetch_data` for fetching and saving rates)
- converter_config.py (configuration such as file paths, URLs, and constants)
- currency_converter.py (imports  `conversion` for conversion processing)
- utils.py (imports `clear_screen`, `show_menu` for UI and processing)

Usage:
- Run the script directly and follow the prompts to convert currencies.
- The program automatically handles missing offline files and can fetch 
  latest rates online if needed.

Author: Avi Lavi
Date: 03-09-2025
"""


import sys
from converter_config import URL, MAIN_MENU
from currency_converter import conversion
from update_from_online import fetch_data
from utils import clear_screan, show_menu



def main():
    clear_screan()
    while True:
        option = show_menu(MAIN_MENU)
        match option:
            case '0':
                sys.exit()
            case '1': 
                conversion()
            case '2': 
                fetch_data(URL)
            case '3': pass
            case '4': pass
            case _: print("Incorrect input")    

if __name__ == "__main__":
    main()
    