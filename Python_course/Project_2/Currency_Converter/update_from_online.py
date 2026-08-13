# update_from_online.py

import sys
import json
import requests
from converter_config import OFF_LINE_DATA_FILE_PATH
from utils import display_message, file_exists


def save_rates_locally(rates: dict) -> None: 
    """
    Saves the given currency rates to the local offline JSON file.

    Parameters:
        rates (dict): Dictionary containing currency conversion rates.
    """
    try:
        with open(OFF_LINE_DATA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump({"rates": rates}, f, indent=4)
        display_message("Rates saved locally for offline use.", "info")
    except Exception as e:
        display_message(f"Failed to save rates locally: {e}", "error")


def fetch_data(url:str):
    """
    Ensures that a local JSON file with currency conversion rates exists.
    If the offline file does not exist, fetches rates from the online service
    and saves them locally for future offline use.
    If the file already exists, asks the user whether to update it.

    Parameters:
        url (str): The API endpoint to fetch currency conversion rates from.

    Returns:
        tuple[dict, int | None]: 
            - (rates, status_code) if the fetch fails or HTTP status code is invalid.
            - ({}, None) if a request exception occurs.
            - May exit the program if offline file exists and user chooses not to update.
            - Note: Does not return anything on successful fetch and local save.
    """
        
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        rates = data.get("conversion_rates")
        
        # Validate status code is in 200–399
        if 200 <= response.status_code < 400:
            if not file_exists(OFF_LINE_DATA_FILE_PATH):
                save_rates_locally(rates)
            else:
                display_message("The file already exists.", "info")
                overwrite_status = input("Do you want to update the rates? Enter 'Y' to update, any other key to quit : ").strip().lower()
                
                if overwrite_status == 'y': 
                    save_rates_locally(rates)
                else: 
                    sys.exit(0)
        else:
            display_message(f"Invalid HTTP status code: {response.status_code}","warning")
            return {}, None

    except requests.exceptions.RequestException as err:
        # Handle any request-related errors
        display_message(f"Web request failed: {err}","highlight")
        return {}, None
  
  
# fetch_data(URL)