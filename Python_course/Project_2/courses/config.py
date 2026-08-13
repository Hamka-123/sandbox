import pathlib
import sys

if __name__ == "__main__":
    print("MODULE: Incorrect call attempt!!!")
    sys.exit(666)

ROOT_FOLDER = pathlib.Path(__file__).parent
STUDENTS_FILE = ROOT_FOLDER.joinpath("students.json")
COMPANY_NAME = "My_company" #new folders root
MAX_GROUP_SIZE = 10
STUDENT_FOLDERS = ["class_work", "home_work", "tmp"]
STUDENT_PERSONAL_DATA_FILE = "student_data.txt" # student name, email, phone
MAIN_MENU = """Choose action:
0 - Exit
1 - get students
2 - get students in courses
3 - get students in groups
4 - create folders
"""