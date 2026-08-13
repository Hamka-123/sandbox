# utils.py

import pathlib
import csv
import os
from datetime import datetime, time
from converter_config import CLEAR_SCREEN, COLORS, ROOT_PATH
import time

def generate_csv_line(*args) -> list:
    """
    This function receives arguments

    Returns:
        Returns a list for CSV file
    """
    values = []
    for item in args:
        values.append(str(item))
    return values


def write_csv_header(filename: str, *args) -> None:
    """
    Write a header row to a CSV file.

    param filename: Name of the CSV file
    param args: Column names for the header
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(args)
        

def file_exists(file_path):
    """
    Check if a file exists.
    
    return: True if exists, False otherwise.
    """
    return os.path.exists(file_path)


def get_current_datetime() -> tuple[str, str]:
    """
    return: (date_str, time_str) in format "YYYY-MM-DD", "HH:MM:SS"
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    return date_str, time_str


def is_file_ready(filename: str):
    """
    Check if a file exists and is not empty.
    """
    return os.path.isfile(filename) and os.path.getsize(filename) > 0


def write_to_csv_log(filename: str, *args):
    """
    Append a row of values to a CSV file.
    """
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(args)


def display_message(message='', level="info"):
    """
    Prints a message to the console in the color corresponding to the given level.
    """
    reset = COLORS.get("reset", "\033[0m")
    color = COLORS.get(level.lower())
    print(f"{color}{message}{reset}")
    
    
def show_menu(menu_items:str) -> None:
    return input(menu_items)

    
def clear_screan():
    """
    Clears the console screen and moves the cursor to the top-left corner.
    """
    print(CLEAR_SCREEN, end="")
   

def get_file_size(filename: str) -> int:
    """
    Return the file size in bytes.
    If the file does not exist, return -1.
    """
    if not os.path.isfile(filename):
        return -1
    return os.path.getsize(filename)


def rename_file(original_filename: str) -> str:
    """
    Rename a file by appending a timestamp to its name.

    param original_filename: The current name of the file.
    return: The new filename after renaming.
    """
    if not os.path.isfile(original_filename):
        display_message(f"File '{original_filename}' does not exist.", "error")
        return ""

    # Split directory and file name with extehsion
    directory, filename = os.path.split(original_filename)
    # Split extension and file name with path
    name, ext = os.path.splitext(original_filename)

    # Generate timestamp (YYYY-MM-DD_HH-MM-SS)
    current_date, current_time = get_current_datetime()
    # ":" Not valid in the filename
    current_time = current_time.replace(":","-")
    timestamp = f"{current_date}_{current_time}"
    
    # Create new filename
    new_filename = f"{timestamp}_{filename}"
    new_file_path = ROOT_PATH.joinpath("Logs").joinpath(new_filename)
    try:
        os.rename(original_filename, new_file_path)
        display_message(f"File renamed to '{new_filename}'.")
        return new_file_path
    except OSError as e:
        display_message(f"Error renaming file: {e}", "error")
        return ""
    
    
def copy_file(file_name:str) -> None:
    pass
    
