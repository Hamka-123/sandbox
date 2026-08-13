#CSV - comma separated values

import pathlib


FILE_NAME = pathlib.Path(__file__).parent.joinpath("data_files", "test1.csv")

with open(FILE_NAME) as f:
    csv_headers = f.readline()
    users = f.readlines()
    
print(csv_headers)
print(users)
#print every user name
for user in users:
    print(user.split(",")[0])
# print every user password
for user in users:
    print(user.split(",")[1])
# print every user email
for user in users:
    print(user.split(",")[2])
