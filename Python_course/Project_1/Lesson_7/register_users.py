# input name, password
# append to users.txt

import json
import pathlib

add_new_user = input("Add new user? (y/n): ")
while add_new_user == "y":
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    add_new_user = input("Add new user? (y/n): ")
    file_name = "users.txt"
    file_path = pathlib.Path(__file__).parent.joinpath("data_files", file_name)
    with open(file_path, "a") as f:
        f.write(f"{name}:{password}\n")
    if add_new_user != "y":
        break



#записать в файл как dict
# with open(file_path, "a") as f:
#     f.write(f"{name}: {password}\n")
#записать в файл как json
# import json
# with open(file_path, "a") as f:
#     json.dump({"name": name, "password": password}, f)



    
