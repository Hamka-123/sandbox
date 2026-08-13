
import re


EMAIL_PATTERN = r'\b(?P<username>\w*)@+(?P<domain>\w*.\w*)'
TARGET_STRING = '''
id,first_name,last_name,email,gender,ip_address
1,D'arcy,Benge,dbenge0@friendfeed.com,Male,93.228.107.140
2,Kelcy,Hakonsson,khakonsson1@washingtonpost.com,Female,181.93.173.27
3,Jerrilee,Velasquez,jvelasquez2@dell.com,Non-binary,212.142.76.100
4,Carola,Pirri,cpirri3@techcrunch.com,Female,220.2.253.47
5,Even,Butterly,ebutterly4@bloglines.com,Male,230.206.172.123
6,Leisha,Shellibeer,lshellibeer5@java.com,Female,82.210.124.168
7,Abdul,Garlette,agarlette6@flickr.com,Male,166.95.106.164
8,Arther,Samet,asamet7@icq.com,Male,190.183.101.142
9,Ev,Mewrcik,emewrcik8@archive.org,Male,49.75.241.142
10,Enrico,Lambin,elambin9@moonfruit.com,Male,5.104.249.62
'''

res = re.search(EMAIL_PATTERN, TARGET_STRING)

print(res)
print(res.start())
print(res.end())
print(res.span())
print(res.group(2))
print(res.groups())

for group in res.groups():
    print(group)
    
res = re.findall(EMAIL_PATTERN, TARGET_STRING)

print(res)

#flags
'''
re.DEBUG
re.MULTILINE
re.DOTALL
re.UNICODE
re.IGNORECASE
re.LOCALE
re.L
re.M
re.A
re.X
re.ASCII
re.NOFLAG
re.S
re.T
re.TEMPLATE
'''

for username, domain in res:
    print(username)
    print(domain)

res = re.finditer(EMAIL_PATTERN, TARGET_STRING)
print(type(res))
print(next(res))


res = re.split(r'^\d+', TARGET_STRING)
print(res)