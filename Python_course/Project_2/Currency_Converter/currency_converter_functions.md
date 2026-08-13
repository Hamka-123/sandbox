# Currency Converter - Function Documentation

This document describes all functions in `currency_converter.py`
including imported utility functions.

------------------------------------------------------------------------

## **Functions in `currency_converter.py`**

### `show_menu()`

Clears the console screen and moves the cursor to the top-left corner.

------------------------------------------------------------------------

### `get_user_input()`

Prompts the user for source and target currencies and an amount to
convert.

**Returns:** - `tuple (from_currency, to_currency, amount)`

------------------------------------------------------------------------

### `read_data_from_file() -> dict`

Reads a JSON file containing currency conversion rates and returns the
data as a dictionary.

**Behavior:** - Asks user if offline conversion should be used when
online service is unavailable. - If the file exists → loads JSON and
returns `rates`. - If the file does not exist → exits program with error
message.

**Returns:** - `dict` of currency rates

------------------------------------------------------------------------

### `read_data_from_web(url: str)`

Fetches conversion rates from an online API.

**Parameters:** - `url (str)`: API endpoint

**Returns:** - `(rates: dict, status_code: int | None)`

**Behavior:** - Validates HTTP status code (200--399). - Returns rates
on success. - On failure, returns `{}` and `None`.

------------------------------------------------------------------------

### `main()`

Main entry point for the program.

**Responsibilities:** - Retrieves conversion rates (online or
offline). - Prompts user input for currencies and amount. - Performs
conversion. - Displays result. - Logs operation (date, time, currencies,
amount, converted value, connection mode).

------------------------------------------------------------------------

## **Imported Utility Functions (from `utils`)**

### `file_exists(path: Path) -> bool`

Checks whether a given file path exists.

------------------------------------------------------------------------

### `generate_line(date, time, from_currency, to_currency, amount, converted_amount, connection_mode) -> tuple`

Generates a tuple representing a line to be logged.

------------------------------------------------------------------------

### `write_csv_header(file_path, *headers)`

Writes a CSV header to a new log file.

------------------------------------------------------------------------

### `get_current_datetime() -> tuple[str, str]`

Returns the current date and time.

------------------------------------------------------------------------

### `validate_file_write(file_path) -> bool`

Validates if the given file can be written to.

------------------------------------------------------------------------

### `write_to_log(file_path, *values)`

Appends a record to the log file.

------------------------------------------------------------------------

### `display_message(message: str, level: str = "info")`

Displays a formatted message to the user.

------------------------------------------------------------------------
