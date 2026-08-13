# employees = []
# add new user
# loop, MAX - 10 users, add new user (ask yes? or no?)
# print all users + user number:
# check the double of role
'''
User N  | User role | Password
-------------------------------
1       | Admin     | sfasf
2       | Operator  | sfasf
3       | New       | sfasf
'''
MAX_EMPLOYEES = 10

employees = [
    ["Admin","test1"],
    ["Operator","test2"]
]

for i in range(MAX_EMPLOYEES-len(employees)):
    decision = int(input('''
                         Add new user?
                         1 - Yes
                         2 - No
                         '''))
    if decision != 1:
        break  
    
    while True: #check the double of role
        employees_name = str(input("Type user role:\n"))
        role_exists = any(employees_name == employee[0] for employee in employees)
        if role_exists:
            print(f"The role '{employees_name}' already exists! Please choose another one.")
        else:
            break 
     
    employees_pass = (str(input("Type user pass:\n")))
    employees.append([employees_name, employees_pass])
        

table_key1 = "User N"
table_key2 = "User role"
table_key3 = "Password"

column_width = max(len(table_key1), len(table_key2), len(table_key3), max(len(user) for user in employees))


table_header = f'{table_key1.center(column_width)} | {table_key2.center(column_width)} | {table_key3.center(column_width)}\n'
table_separator = f'{"-"*(column_width*3 + 6)}\n'

table = f'{table_header}{table_separator}'

for i in range(len(employees)):
    row = f'{str(i+1).center(column_width)} | {employees[i][0].center(column_width)} | {employees[i][1].center(column_width)}\n'
    table += row
    
print(table)