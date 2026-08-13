
# mailing protocols
'''
SMTP (Simple Mail Tranfer Protocol) -> send
POP3 (Post Office Protocol V3)    -> receive (download)
IMAP (internet Message Access Protocol) -> synchronize messages


Gmail settings
IMAP server at imap.gmail.com:993
POP server at pop.gmail.com:995 require SSL. 
outgoing SMTP server, smtp.gmail.com, supports TLS
use port 465 (for SSL), or port 587 (for TLS)

SMTP server access:
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "java2069.mailer.test@gmail.com"
SMTP_PASSWORD = "tifr enip gakg syuo"

'''
from dotenv import load_dotenv
import os
load_dotenv()

import smtplib

SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')

#SMTP_HOST = '2a00:1450:400c:c06::6d'
SMTP_HOST = 'smtp.gmail.com' #partner provider не обрабатывает быстро, Golan нормально.
SMTP_PORT = 587


TEXT_MESSAGE = f'''\
subject: first test
To: {SMTP_USER}
From: {SMTP_USER}

Hello world!!! from Alina 3
'''


#connect
with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    server.starttls()
    server.login(SMTP_USER, SMTP_PASS)
    errs = server.sendmail(SMTP_USER,SMTP_USER,TEXT_MESSAGE)
    if not errs:
        print("ok")
    else: print(errs)



"""
#structured email 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "java2069.mailer.test@gmail.com"
SMTP_PASSWORD = "tifr enip gakg syuo"


TEXT_MESSAGE = '''\
subject: First test
To: java2069.mailer.test@gmail.com
From: java2069.mailer.test@gmail.com

Hello world !!!
   
'''

# create message object
message = MIMEMultipart()
message["Subject"] = "Multipart message test"
message["From"] = SMTP_USER
message["To"] = SMTP_USER

msg_text_body = '''\
subject: First test
To: java2069.mailer.test@gmail.com
From: java2069.mailer.test@gmail.com

Hello world - Text message part !!!
   
'''
msg_html_body = '''
<h1 style='color: red'>HTML header</h1>
TEST TEXT
'''
message.attach(MIMEText(msg_text_body, "plain"))
message.attach(MIMEText(msg_html_body, "html"))

"""
"""
# connect
with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    try:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [SMTP_USER, "qababenko@gmail.com", "nyurkadu@gmail.com", "roman65@gmail.com"], message.as_string())
        pass
    except Exception as e:
        print(e)
        pass 
    pass

print("FINISHED")
"""


#Debugging
"""
import smtplib
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "java2069.mailer.test@gmail.com"
SMTP_PASSWORD = "tifr enip gakg syuo"

TEXT_MESSAGE = '''\
subject: First test
To: java2069.mailer.test@gmail.com
From: java2069.mailer.test@gmail.com
Hello world !!!
   
'''
# connect
with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    try:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, "qababenko@gmail.com", TEXT_MESSAGE)
        pass
    except Exception as e:
        print(e)
        pass 
    pass
print("FINISHED")
"""
"""
import smtplib
import socket
import sys

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "java2069.mailer.test@gmail.com"
SMTP_PASSWORD = "tifr enip gakg syuo"

def debug_smtp_connection():
    print("=== ДИАГНОСТИКА SMTP СОЕДИНЕНИЯ ===")
    
    # 1. Проверяем доступность хоста
    try:
        print("1. Проверяем доступность smtp.gmail.com...")
        test_socket = socket.create_connection((SMTP_HOST, SMTP_PORT), timeout=5)
        test_socket.close()
        print("   ✅ Хост доступен")
    except socket.error as e:
        print(f"   ❌ Хост недоступен: {e}")
        return False

    # 2. Пробуем установить соединение с дебагом
    try:
        print("2. Устанавливаем SMTP соединение...")
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        server.set_debuglevel(1)  # Включаем детальный вывод
        print("   ✅ Соединение установлено")
        
        print("3. Запускаем TLS...")
        server.starttls()
        print("   ✅ TLS запущен")
        
        print("4. Пробуем логин...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("   ✅ Логин успешен")
        
        # Короткое сообщение
        message = '''Subject: Test
To: qababenko@gmail.com
From: java2069.mailer.test@gmail.com

Test message'''
        
        print("5. Отправляем сообщение...")
        server.sendmail(SMTP_USER, "qababenko@gmail.com", message)
        print("   ✅ Сообщение отправлено")
        
        print("6. Закрываем соединение...")
        server.quit()
        print("   ✅ Соединение закрыто")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False

# Запускаем диагностику
if debug_smtp_connection():
    print("✅ ВСЕ ОПЕРАЦИИ ВЫПОЛНЕНЫ УСПЕШНО")
else:
    print("❌ ВОЗНИКЛИ ПРОБЛЕМЫ")
    
"""

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pathlib
import smtplib

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "java2069.mailer.test@gmail.com"
SMTP_PASSWORD = "tifr enip gakg syuo"


# create message object
message = MIMEMultipart()
message["Subject"] = "Multipart message test"
message["From"] = SMTP_USER
message["To"] = SMTP_USER

msg_text_body = '''\
subject: First test
To: java2069.mailer.test@gmail.com
From: java2069.mailer.test@gmail.com

Hello world - Text message part !!!
   
'''

text_part = MIMEText(msg_text_body, "plain")

msg_html_body = '''
<h1 style='color: red'>HTML header</h1>

'''

with open(pathlib.Path(__file__).parent.joinpath("message.html")) as f:msg_html_body = f.read() 


html_part = MIMEText(msg_html_body, "html")

# Add attachment
ATTACHMENT_FILE = "Python_advanced_.pdf"
with open(pathlib.Path(__file__).parent.joinpath(ATTACHMENT_FILE), 'rb') as f: 
    binary_part = MIMEBase("application", "octet-stream")
    binary_part.set_payload(f.read())
    pass
encoders.encode_base64(binary_part)
binary_part.add_header(
    "Content-Disposition",
    f'attachment; filename= {ATTACHMENT_FILE}'
)

message.attach(text_part) # message  part 1 -> text part
message.attach(html_part) # message part 2 -> HTML part
message.attach(binary_part) # binary part - attachment




# connect
with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    try:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [SMTP_USER, "qababenko@gmail.com", "nyurkadu@gmail.com", "roman65@gmail.com"], message.as_string())
        pass
    except Exception as e:
        print(e)
        pass 
    pass

print("FINISHED")