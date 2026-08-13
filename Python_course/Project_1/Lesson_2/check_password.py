SECRET_PASSWORD = "qwerty123"

user_password = input("Enter password\n")

if user_password == SECRET_PASSWORD:
    print("Access granted \u2705")
else:
    print("Access denied \u274C")