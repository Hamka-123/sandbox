import re

time_pattern = re.compile(r'^(?:[0-9]|1[0-9]|2[0-3])[^\d](?:[0-5]?[0-9])$')

while True:
    time = input("Enter time HH:MM ").strip()
    match = re.match(time_pattern, time)
    if match:
        #hours, minutes = re.split(r'[^\d]',time)
        hours = match.group(1)
        minutes = match.group(2)
        print(f'''
              Hours: {hours}
              Minutes: {minutes}
              ''')
        break
    else:
        print("Not correct format, try again...")
    