# curency_converter.py

import json
import requests
import sys
from utils import (
    file_exists,
    generate_csv_line,
    get_file_size,
    rename_file,
    write_csv_header,
    get_current_datetime,
    is_file_ready,
    write_to_csv_log,
    display_message,
    clear_screan
)
from converter_config import OFF_LINE_DATA_FILE_PATH, HISTORY_LOG_FILE_PATH, URL, LOG_FILE_HEADER
from converter_config import CLEAR_SCREEN, MAX_FILE_SIZE



    
def get_user_input():
    """
    Prompt user for source and target currencies and an amount to convert.
    
    Returns:
        tuple: (from_currency, to_currency, amount)
    """
    while True:
        user_input = input("Enter source currency, target currency, and amount (e.g., USD EUR 100) or Q to quit:").strip()
        
        if user_input.upper() == "Q":
            print(CLEAR_SCREEN, end="")
            display_message("Exiting program.")
            sys.exit(0)
        
        parts = user_input.split()
        if len(parts) != 3:
            clear_screan()
            display_message("Please enter exactly 3 values (source, target, amount).","info")
            continue
        
        from_currency, to_currency, amount = parts
        if not amount.isdigit(): 
            clear_screan()
            display_message("Amount must be a number.","info")
            continue
        
        return from_currency.upper(), to_currency.upper(), amount


def read_data_from_json_file() -> dict:
    """
    Reads a JSON file containing currency conversion rates and returns the data as a dictionary.
    """
    user_answer = input(f"Online service is currently unavailable. Use offline conversion? (Y/N):").strip().lower()
    
    if user_answer in ('y', 'yes'):
        if file_exists(OFF_LINE_DATA_FILE_PATH):
            with open(OFF_LINE_DATA_FILE_PATH , "r", encoding="utf-8") as f:
                return json.load(f).get("rates", {})
        else:
            display_message("File does not exists. Exiting program.", "error")
            sys.exit(0)
    else:
        display_message("Exiting program.","reset")
        print(CLEAR_SCREEN, end="")
        sys.exit(0)
        

def read_data_from_web(url: str):
    try:
        response = requests.get(url, timeout=10)
        
        # Validate status code is in 200–399
        if 200 <= response.status_code < 400:
            data = response.json()
            rates = data.get("conversion_rates")
            return rates, response.status_code
        else:
            display_message(f"Invalid HTTP status code: {response.status_code}","warning")
            return {}, None

    except requests.exceptions.RequestException as err:
        # Handle any request-related errors
        display_message(f"Web request failed: {err}","highlight")
        return {}, None  

  
def conversion():
    """
    Retrieve currency data (online or offline), convert an amount, and log the operation.
    """
    clear_screan()
    
    data, code = read_data_from_web(URL)
    if data and code is not None:
        connection_mode = "On-Line"  
    else:
        data = read_data_from_json_file()
        connection_mode = "Off-Line"
        
    source_currency, target_currency, amount = get_user_input() 
  
    if (source_currency in data) and (target_currency in data):
        source_rate = float(data[source_currency])
        target_rate = float (data[target_currency])
        
        converted_amount = int(amount) * (float((target_rate)) / (float(source_rate)))
        # rounded_amount = round(converted_amount, 2)
        display_message(f"The final amount {converted_amount:*>10.2f} {target_currency}")
        
        date, time = get_current_datetime()
        
        line_to_log = generate_csv_line(date, time, source_currency, source_rate, target_currency, target_rate, amount, converted_amount, connection_mode )

        #                     0     1     2       3       4      5        6          7       8
        LOG_LINE_FORMAT = "{:<10},{:<8},{:<5},{:<15.2f},{:<5},{:<15.2f},{:>15.2f},{:>15.2f},{:<10}"
        
        formatted_line = LOG_LINE_FORMAT.format(
        line_to_log[0],         # date
        line_to_log[1],         # time
        line_to_log[2],         # from_cur
        float(line_to_log[3]),  # from_cur_amount
        line_to_log[4],         # to_cur
        float(line_to_log[5]),  # to_cur_amount
        float(line_to_log[6]),  # amount
        float(line_to_log[7]),  # converted_amount
        line_to_log[8]          # connection_mode
        )
        
        list_1 = formatted_line.split(",")
        list_to_print =[item.strip() for item in list_1]
         
        if not file_exists(HISTORY_LOG_FILE_PATH):
            logs_folder = HISTORY_LOG_FILE_PATH.parent
            logs_folder.mkdir(parents=False, exist_ok=True)
            write_csv_header(HISTORY_LOG_FILE_PATH, *LOG_FILE_HEADER)
        
        if is_file_ready(HISTORY_LOG_FILE_PATH):
            if get_file_size(HISTORY_LOG_FILE_PATH) > MAX_FILE_SIZE:
                rename_file(HISTORY_LOG_FILE_PATH)
                write_csv_header(HISTORY_LOG_FILE_PATH, *LOG_FILE_HEADER)
            # write_to_csv_log(HISTORY_LOG_FILE_PATH, *line_to_log)
            write_to_csv_log(HISTORY_LOG_FILE_PATH, *list_to_print)
            
    else:
        display_message(f"One of the currencies {source_currency} or {target_currency} does not exist.", "error")
      

#conversion()