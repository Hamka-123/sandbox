# input email haim@gmail.com
# convert -> h...@gmail.com
'''
email = input("Enter an email address: ")
username, domain = email.split("@")
converted_email = f"{username[0]}...@{domain}"
print(converted_email)
'''
# only with string methods
email = input("Enter an email address: ")

# ЕСЛИ в строке есть НЕ ASCII символы - надо обратботать строку чтобы убрать 
# оттуда эти символы с использованием только методов работы со строками
if not email.isascii():
    email = email.encode('ascii', errors='ignore').decode('ascii')
    
#get @ index
at_index = email.index("@")
#get domain
domain = email[at_index:]
#get name
name = email[:at_index]
#dots count = count symbols after 0 index
dots_count = len(name) -1
#convert email
converted_email = name[0] + "." * dots_count + domain

print(converted_email)