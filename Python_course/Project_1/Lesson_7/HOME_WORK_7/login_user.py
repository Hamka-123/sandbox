# input name, password
# check in file
# access granted / denied
import pathlib

login = input("Enter your login: ")
password = input("Enter your password: ")

FILE_NAME = pathlib.Path(__file__).parent.parent.joinpath("data_files", "users.txt")

with open(FILE_NAME) as f:
    users = f.readlines()
    for i in range(len(users)):
        users[i] = users[i].strip().split(":")
 
# convert to list[dict] all users in file
users_obj = []
for user in users:
    user_obj = {
        "login": user[0],
        "password": user[1],
    }
    users_obj.append(user_obj)
    
#check if user exists - grant access else denied
access = False
for user in users_obj:
    if user["login"] == login and user["password"] == password:
        access = True
        break
if access:
    print("Access granted")
else:
    print("Access denied")
