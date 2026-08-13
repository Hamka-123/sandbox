import sys
from collections import defaultdict
from typing import Dict, List

if __name__ == "__main__":
    print("MODULE: Incorrect call attempt!!!")
    sys.exit(666)


def create_groups(data: dict, max_group_size) -> dict[str, dict[str, dict]]:
    """create dict of courses, primary key = course {groups - dict[dict] primary_key = ID}"""
    courses: Dict[str, List[str]] = defaultdict(list)
    # Собираем студентов по курсам
    for student in data.values():
        course = student.get("course", "Unknown")
        courses[course].append(student["first_name"] + "_" + student["last_name"])

    # Разбиваем на группы с уникальным ID
    grouped_courses: Dict[str, dict] = {}
    for course, students in courses.items():
        grouped_courses[course] = {}
        group_id = 1
        for i in range(0, len(students), max_group_size):
            grouped_courses[course][f"{course}_group_{group_id}"] = students[i:i + max_group_size]
            group_id += 1
    return courses, grouped_courses