#read JSON
#convert to python object
#change data (add new user)
#save to JSON file

import json
import pathlib

#read JSON
json_file_path = pathlib.Path(__file__).parent / 'users.json'
with open(json_file_path, 'r') as file:
    #convert to python object 
    data = json.load(file)
print(type(data))
#change data (add new user)
next_id = max(user['id'] for user in data) + 1
'''
new_user = {
    "id": next_id,
    "first_name": "John Doe",
    "last_name": "Smith",
    "email": "test@mail.com",
    "gender": "New",
    "ip_address": "111.111.111.111"
}
'''
#v.2 - receive new user data from console input
new_user = {
    "id": next_id,
    "first_name": input("Enter first name: "),
    "last_name": input("Enter last name: "),
    "email": input("Enter email: "),
    "gender": input("Enter gender: "),
    "ip_address": input("Enter ip address: ")
}

data.append(new_user)
#save to JSON file
with open(json_file_path, 'w') as file:
    json.dump(data, file, indent=4)
    
print("\nNew user has been added to the JSON file.")
print(new_user)
