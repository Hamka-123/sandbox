#read string from file
#✅TODO: Task 1: get all mails, mailnames, maildomains using regular expressions
#✅TODO: Task 2: replace all emails to corporate mails, save to csv file
## corporate emails: firstname.lastname@mycorp.com

import pathlib
import re

#TASK 1
FILE_NAME = 'MOCK_DATA (12).csv'
FILE_PATH = pathlib.Path(__file__).parent.joinpath(FILE_NAME)

with open(FILE_PATH, 'r') as f:
    header = f.readline().strip()
    file_data = f.read().strip()
    
print(type(file_data))
print(header)
print(f'{'-'*20}')

mails_regex = r'\b(?P<mails>\w*@+\w*.\w*)'
mails = re.findall(mails_regex, file_data)
print(mails)
print(f'{'-'*20}')

mailnames_regex = r'\b(?P<username>\w*)@'
mailnames = re.findall(mailnames_regex, file_data)
print(mailnames)
print(f'{'-'*20}')

maildomains_regex = r'\b@+(?P<domain>\w*.\w*)'
maildomains = re.findall(maildomains_regex, file_data)
print(maildomains)
print(f'{'-'*20}')

#TASK 2
#разбиваем на подстроки
pattern = r'(\d+),([^,]+),([^,]+),([^,]+),([^,]+),([\d.]+)'
# Находим все совпадения
matches = re.findall(pattern, file_data)

results = []
for match in matches:
    
    results.append({
        'id': match[0],
        'first_name': match[1],
        'last_name': match[2],
        'email': match[3],
        'gender': match[4],
        'ip': match[5]
    })
    
parsed_data = results

# Создаем копию данных для замены
new_file_data = file_data

for person in parsed_data:
    new_mails = f'{person['first_name']}.{person['last_name']}@mycorp.com'.replace("'", "").lower()
    
    if int(person['id']) <=10:
        # Логируем замену
        print(f"{person['id']} {person['first_name']} {person['last_name']:12}")
        print(f"   БЫЛО: {person['email']}")
        print(f"   СТАЛО: {new_mails}")
    
    new_file_data = re.sub(
            re.escape(person['email']), 
            new_mails, 
            new_file_data
        )

NEW_FILE = FILE_PATH.parent.joinpath(f'CORPORATE_{FILE_NAME}')

with open(NEW_FILE, 'w') as f: 
    f.write(header + '\n') 
    f.writelines(new_file_data)
    


