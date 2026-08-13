import sys
import json
import pathlib


if __name__ == "__main__":
    print("MODULE: Incorrect call attempt!!!")
    sys.exit(666)


def get_students(file: pathlib.Path)  -> dict[str, dict]:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f) # list[dict]
        students = {student["first_name"]+"_"+student["last_name"]:student for student in data}
        return students