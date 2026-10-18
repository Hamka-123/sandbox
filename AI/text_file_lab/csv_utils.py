# Start
# |
# v
# Create output CSV path
# |
# v
# Prepare column headers
# |
# v
# Prepare records
# |
# v
# Open CSV file
# |
# v
# Create csv.writer
# |
# v
# Write header
# |
# v
# Write records
# |
# v
# Close file
# |
# v
# Display result
# |
# v
# End

# • csv.writer
# • CSV headers
# • rows
# • newline=""
# • UTF-8 encoding
# • pathlib

import csv
from pathlib import Path


def create_sample_csv(file_path):
    """
    Create a sample AI engineering CSV dataset.
    """
    # Create output CSV path using pathlib
    path = Path(file_path)

    # 1. Define the column headers
    headers = ["id", "model_name", "task_type", "latency_ms", "status"]

    # 2. Define several records (rows)
    records = [
        [1, "gemini-3.6-flash", " text-generation ", 120, "success"],
        [2, "gemini-3.6-flash", " summarization ", 250, "success"],
        [3, "gemini-3.6-flash", " classification ", 95, "success"],
    ]

    # 3. Open the file using UTF-8 encoding and newline=""
    with open(path, mode="w", encoding="utf-8", newline="") as csv_file:
        # 4. Create csv.writer
        writer = csv.writer(csv_file)

        # 5. Write the header
        writer.writerow(headers)

        # 6. Write all records
        writer.writerows(records)

    # Display result
    print(f"Sample CSV successfully created at: {path}")


def clean_records(records):
    """
    Clean and validate CSV records.
    """
    cleaned_records = []

    # Read record and check for more records
    for record in records:
        if not record:
            continue

        is_valid = True
        cleaned_row = []

        # Check required fields
        for value in record:
            if value is None:
                # Mark invalid if field is missing/None
                is_valid = False
                break

            if isinstance(value, str):
                # Remove surrounding whitespace
                cleaned_value = value.strip()
                if not cleaned_value:
                    is_valid = False
                    break
                cleaned_row.append(cleaned_value)
            else:
                cleaned_row.append(value)

        # Add cleaned record if valid
        if is_valid:
            cleaned_records.append(cleaned_row)

    # Return cleaned records
    return cleaned_records
