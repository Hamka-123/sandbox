import pathlib
from class_student import *

#read CSV
data_file = pathlib.Path(__file__).parent.joinpath("MOCK_DATA (13).csv")
#print(data_file)

with open(data_file) as f:
    header = f.readline()
    data = f.readlines()
    
print(type(data))
print(data[0])

#create list [Student] 
list_obj_student = []

for student in data:
    fields = student.strip().split(',')
    
    if len(fields) >=6:
        student_obj = Student(
            fields[0], # first_name
            fields[1], # last_name 
            fields[2], # email
            fields[3], # gender
            fields[4], # course
            fields[5]  # balance
            
        )
        list_obj_student.append(student_obj)
        
print(list_obj_student[0].id)
print(list_obj_student[0].first_name)
print(list_obj_student[0].last_name)
print(list_obj_student[0].email)
print(list_obj_student[0].gender)
print(list_obj_student[0].course)
print(list_obj_student[0].balance)

print(list_obj_student[0].get_full_name())

first_id = list_obj_student[0].id
print(first_id)

new_balance = list_obj_student[0].update_balance(50)

print(f'New balance of {first_id} = {new_balance}')

# v.2
with open(data_file) as f:
    students = [StudentV2(*stud_data_string.strip().split(",")) for stud_data_string in f.readlines()[1:]]  
    
print(students[1])
print(students[1].check_balance())

