# enter login name
# check no spaces
# max attempts = 5

MAX_ATTEMPTS = 5



for i in range(MAX_ATTEMPTS):
    login_name = input("Enter your login name: ")
    if login_name.count(" ") == 0:
        print(f"Login name accepted {login_name}")
        break