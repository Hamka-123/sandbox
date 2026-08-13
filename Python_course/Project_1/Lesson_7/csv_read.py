#read file
# convert to list[list[str]]


import pathlib


FILE_NAME = pathlib.Path(__file__).parent.joinpath("data_files", "MOCK_DATA (3).csv")

with open(FILE_NAME) as f:
    csv_headers = f.readline()
    users = f.readlines()
    for i in range(len(users)):
        users[i] = users[i].strip().split(",")
        


'''
#v.1 - read file and convert to list[list[str]]
print(csv_headers)
users = users[:10] # limit to 10 users
print(users)

# print every user data
for user in users:  
    print(f'{user[0]} - {user[1]} - {user[2]} - {user[3]} - {user[4]} - {user[5]}')

# convert to list[dict] 

users_obj = []
for user in users:
    user_obj = {
        "id": user[0],
        "first_name": user[1],
        "last_name": user[2],
        "email": user[3],
        "gender": user[4],
        "ip_address": user[5],
    }
    users_obj.append(user_obj)

#print user object
for user in users_obj:
    print(user)
'''



# convert to list[dict] all users in file
users_obj = []
for user in users:
    user_obj = {
        "id": user[0],
        "first_name": user[1],
        "last_name": user[2],
        "email": user[3],
        "gender": user[4],
        "ip_address": user[5],
    }
    users_obj.append(user_obj)
'''
#v.2 - find user from input by email
email = input("Enter email: ")
for user in users_obj:
    if user["email"] == email:
        print(user)
        break
    
#v.3 - find all users Male genders and save to other file
for user in users_obj:
    if user["gender"] == "Male":
        with open(pathlib.Path(__file__).parent.joinpath("data_files", "Males.csv"), "a") as f:
            f.write(f'{user["id"]},{user["first_name"]},{user["last_name"]},{user["email"]},{user["gender"]},{user["ip_address"]}\n')

#read Males.csv
with open(pathlib.Path(__file__).parent.joinpath("data_files","Males.csv")) as f:
    csv_headers = f.readline()
    users = f.readlines()
    print(csv_headers)
    print(users)
    
'''
#v.4 - change some users and save new file
user_id_for_change = input("Enter user id: ")

field_to_change = input("""
      Enter what fields to change you want: 
      1 - first name
      2 - last name
      3 - email
      4 - gender
      5 - ip address
      6 - all
      7 - exit
      Enter your choice:
      """)
match field_to_change:
    case "1":
        new_first_name = input("Enter new first name: ")
    case "2":
        new_last_name = input("Enter new last name: ")
    case "3":
        new_email = input("Enter new email: ")
    case "4":
        new_gender = input("Enter new gender: ")
    case "5":
        new_ip = input("Enter new ip address: ")
    case "6":
        new_first_name = input("Enter new first name: ")
        new_last_name = input("Enter new last name: ")
        new_email = input("Enter new email: ")
        new_gender = input("Enter new gender: ")
        new_ip = input("Enter new ip address: ")
    case "7":
        print("Exit")
        exit()

for user in users_obj:
    if user["id"] == user_id_for_change:
        if field_to_change == "1":
            user["first_name"] = new_first_name
        elif field_to_change == "2":
            user["last_name"] = new_last_name
        elif field_to_change == "3":
            user["email"] = new_email
        elif field_to_change == "4":
            user["gender"] = new_gender
        elif field_to_change == "5":
            user["ip_address"] = new_ip
        elif field_to_change == "6":
            user["first_name"] = new_first_name
            user["last_name"] = new_last_name
            user["email"] = new_email
            user["gender"] = new_gender
            user["ip_address"] = new_ip
        else:
            print("Invalid choice")
            exit()  
            
        print(f"Changed user: {user}")

# save to new file         
with open(pathlib.Path(__file__).parent.joinpath("data_files", "new_users.csv"), "w") as f:
    f.write(csv_headers)
    for user in users_obj:
        f.write(f'{user["id"]},{user["first_name"]},{user["last_name"]},{user["email"]},{user["gender"]},{user["ip_address"]}\n')
            
