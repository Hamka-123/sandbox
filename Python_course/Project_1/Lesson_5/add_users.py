#adding new user
# ask: add new user? [y]
# add new user
# while say stop = print all and stop 

users = []

USER_MENU = '''Select
0 - Exit
1 - Add user
2 - Remove user
:'''

while True:
    command = input(USER_MENU)
    if command == "1":
        while True:
            new_user = input("Enter user name to add: ")
            user_exists = any(new_user == user for user in users)
            if user_exists:
                print(f"User '{new_user}' already exists. Try again.")
            else:
                users.append(new_user)
                break
    elif command == "0":
        print(f"Added users: {users}")
        break
    elif command == "2":
        user_to_remove = input("Enter user name to delete: ")
        users.remove(user_to_remove)
    else:
        print("Unknown command")


        
