# read log file
# get all ERROR (INFO, WARNING) messages
# split into: (date, message_type, message_text)
import pathlib
import re


LOG_FILE = pathlib.Path(__file__).parent.joinpath('test_log1.log')
LOG_TEMPLATE = r'^(?P<datetime>.*),\s*(?P<lvl>[A-Z]*)\s*,\s*(?P<msg>.*)$'
LOG_LINE_TEMPLATE = r'^(?P<date>[\d]{4}\-[\d]{2}\-[\d]{2})\s*(?P<time>[\d:,]+),\s*(?P<lvl>[A-Z]*)\s*,\s*(?P<msg>.*)$'
LOG_ERROR_TEMPLATE = r'^(?P<datetime>.*),\s*(?P<lvl>WARNING|ERROR|CRITICAL)\s*,\s*(?P<msg>.*)$'

template_select = 'LOG_LINE_TEMPLATE'
    
with open(LOG_FILE, 'r') as f:
    data = f.read().strip()

if LOG_ERROR_TEMPLATE.find('<time>'):
    print("yes")
    
def process_template(template, data):

    pass

if template_select == 'LOG_TEMPLATE' or 'LOG_ERROR_TEMPLATE':
    matches = re.finditer(LOG_TEMPLATE, data, re.MULTILINE)
    logs = []
    for match in matches:
        logs.append({
            "date": match.group('datetime'),
            "message_type": match.group('lvl'),
            "message_text": match.group('msg')
        })
    info = [l.items() for l in logs if l['message_type'] == 'INFO']
    debug = [l.items() for l in logs if l['message_type'] == 'DEBUG']
    #...
    print(info)
    print(f'{'-'*20}') 
        
elif template_select == 'LOG_LINE_TEMPLATE':
    matches = re.finditer(LOG_LINE_TEMPLATE, data, re.MULTILINE)
    logs = []
    for match in matches:
        logs.append({
            "date": match.group('date'),
            "time": match.group('time'),
            "message_type": match.group('lvl'),
            "message_text": match.group('msg')
        })
    def print_dict_of_errors_types(logs):
        # Уникальные типы сообщений
        levels = set(l['message_type'] for l in logs)
        print(levels)

        # Вложенный словарь через dict comprehension
        logs_nested = {
            lvl: {
                idx: {
                    "date": l['date'],
                    "time": l['time'],
                    "message_text": l['message_text']
                }
                for idx, l in enumerate(logs) if l['message_type'] == lvl
            }
            for lvl in levels
        }   
        print(logs_nested)
        
    print_dict_of_errors_types(logs)
    
       
        





 

