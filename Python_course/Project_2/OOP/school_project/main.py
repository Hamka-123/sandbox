import pathlib
from class_school import School

# === MAIN ===  
school = School()
data_file = pathlib.Path(__file__).parent.joinpath("class_student","MOCK_DATA (13).csv")


print(school.get_school_info())
school.get_courses_info()
school.get_groups_info()

school.import_students_from_csv(data_file)
school.fill_courses_from_students()

print(school.students["woda0@smugmug.com"].first_name)  # "Way"

school.add_student('Alina', 'Babenko', 'qababenko@gmail.com', 'female', 'DevOps', '500')

print(school.students["qababenko@gmail.com"].first_name)

# Обновление нескольких полей
school.update_student(
    email='qababenko@gmail.com',
    first_name='AAA', 
    last_name='BBB', 
    course='DevOps Advanced',
    balance='1000'
)

# Обновление одного поля
school.update_student(
    email='qababenko@gmail.com',
    course='Python'
)

#school.delete_student('qababenko@gmail.com')

# Получить последних N студентов
students_list = list(school.get_all_students().values())
print(students_list[-2:])

#print(school.students.keys())

school.add_group(
    'DevOps_2025_001',
    'Devops'
)
school.add_student_to_group(1,'qababenko@gmail.com')
school.add_student_to_group(1,'qababenko@gmail.com')
school.add_student_to_group(1,'woda0@smugmug.com')
school.add_student_to_group(1,'woda0@smugmug.com')
school.update_student(
            email = 'qababenko@gmail.com',
            course = 'Devops'
        )
school.update_student(
            email = 'woda0@smugmug.com',
            course = 'Devops'
        )
school.get_groups_info()
print(school.groups[1].attended_students)
school.remove_student_from_group(1,'woda0@smugmug.com')
school.remove_student_from_group(1,'woda0@smugmug.com')

school.get_courses_info()
