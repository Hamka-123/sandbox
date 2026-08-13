import re

TEMPLATE = re.compile(r'(\b[A-Z][a-z]+\b)')
SEPARATOR = re.compile(r'[\W_]+')

inp_string = input("Enter names: ")
users = re.split(SEPARATOR, inp_string)
print(users)


    

