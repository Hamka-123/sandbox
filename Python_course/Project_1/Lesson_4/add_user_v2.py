# user_list = []
# add new user
# loop, MAX - 10 users, add new user (ask yes? or no?)
# print all users + user number:
'''
User N  | User name
-------------------
1       | Haim
2       | Bob
3       | New
'''

user_list = [
    "Admin",
    "Operator"
]

for i in range(10-len(user_list)):
    decision = int(input('''
                         Add new user?
                         1 - Yes
                         2 - No
                         '''))
    if decision != 1:
        break    
    user_list.append(str(input("Type user name:\n")))
        

table_key1 = "User N"
table_key2 = "User name"

column_width = max(len(table_key1), len(table_key2), max(len(user) for user in user_list))


table_header = f'{table_key1.rjust(column_width)} | {table_key2.ljust(column_width)}\n'
table_separator = f'{"-"*(column_width*2 + 3)}\n'

table = f'{table_header}{table_separator}'

for i in range(len(user_list)):
    row = f'{str(i+1).rjust(column_width)} | {user_list[i].ljust(column_width)}\n'
    table += row
    
print(table)