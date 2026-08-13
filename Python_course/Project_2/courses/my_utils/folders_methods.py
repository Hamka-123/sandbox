import os
import sys

if __name__ == "__main__":
    print("MODULE: Incorrect call attempt!!!")
    sys.exit(666)

def create_workfolders(COMPANY_NAME, groups, students, STUDENT_FOLDERS, ROOT_FOLDER) -> str:
    '''
    -company_name
    --course1_name
    ---group1_ID
    ----student_name
    -----student_data.txt
    -----work_folders_subtree
    '''
    COMPANY_FOLDER = ROOT_FOLDER.joinpath(COMPANY_NAME.upper())
    if COMPANY_FOLDER.exists() == False:
        os.mkdir(COMPANY_FOLDER)
        
    for course_name, course_groups in groups.items():
        course_folder = COMPANY_FOLDER.joinpath(course_name)
        #course_folder.mkdir(exist_ok=True)
        print(f"├─ {course_name}")
        for group_id, group_students in course_groups.items():
            group_folder = course_folder.joinpath(group_id)
            #group_folder.mkdir(exist_ok=True)
            print(f"│  ├─ {group_id}")
            for student_name in group_students:
                student_folder = group_folder.joinpath(student_name)
                #student_folder.mkdir(exist_ok=True)
                print(f"│  │  ├─ {student_name}")
                student_info = students.get(student_name, {})
                print(f"│  │  │  ├─ student_data.txt == {student_info}")
                '''
                # Создать файл student_data.txt
                student_data_file = student_folder.joinpath("student_data.txt")
                with open(student_data_file, "w", encoding="utf-8") as f:
                    student_info = students.get(student_name, {})
                    for k, v in student_info.items():
                        f.write(f"{k}: {v}\n")
                '''
                #создать рабочие папки
                for folder in STUDENT_FOLDERS:
                    STUDENT_FOLDERS_PATH = student_folder.joinpath(folder)
                    #STUDENT_FOLDERS_PATH.mkdir(exist_ok=True)
                    print(f"│  │  │  ├─ {folder}")
                    