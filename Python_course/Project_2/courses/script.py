import sys
from config import *
from my_utils.students_methods import get_students
from my_utils.groups_methods import create_groups
from my_utils.folders_methods import create_workfolders

if __name__ != "__main__":
    print("MAIN MODULE: Incorrect call attempt!!!")
    sys.exit(666)
    
    
while True:
    students = get_students(STUDENTS_FILE)
    courses, groups = create_groups(students, MAX_GROUP_SIZE)
    match input(MAIN_MENU):
        case "0":
            break
        case "1":
            i = 1
            for name, student_data in students.items():
                print(f"\nCтудент {i}: {name} -> {student_data}")
                i +=1
        case "2":
            for course, students in courses.items():
                print(f"\nКурс: {course} ({len(students)})\n","-"*10)
                idx = 1
                for s in students:
                    print(idx,s,"\n")
                    idx += 1
        case "3":
            for course, course_groups in groups.items():
                print(f"\nКурс: {course} ({len(course_groups.items())})\n","-"*10)
                for group_id, group in course_groups.items():
                    # group_id — уникальный id группы
                    # group — список студентов ("first_last name")
                    print(f"  {group_id}: {group}")
        case "4":
            create_workfolders(COMPANY_NAME, groups, students, STUDENT_FOLDERS, ROOT_FOLDER)
        case _:
            print("Некорректный выбор. Попробуйте снова.")

  



  


