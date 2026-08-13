import json
import pathlib
import re
from typing import List

def load_templates_from_folder(templates_folder: str) -> List[str]:
    """Динамически загружает шаблоны из папки и возвращает список имен"""
    templates_path = pathlib.Path(__file__).parent.joinpath(templates_folder)
    
    if not templates_path.exists():
        print(f"⚠️ Templates folder not found: {templates_folder}")
        return []
    
    templates = []
    template_files = list(templates_path.glob('*.html'))
    
    for template_file in template_files:
        template_name = template_file.stem  # Имя файла без расширения
        templates.append(template_name)
        #print(f"📝 Found template: {template_name}")
    
    return templates

def get_template_content(config, template_name: str) -> str:
    """Возвращает содержимое шаблона по имени"""
    templates_path = pathlib.Path(__file__).parent.joinpath(config['EMAIL_TEMPLATES_FOLDER'])
    
    template_file = templates_path / f"{template_name}.html"
    if not template_file.exists():
        available_templates = config['EMAIL_TEMPLATES']
        raise FileNotFoundError(
            f"Template '{template_name}' not found. "
            f"Available templates: {available_templates}"
        )
    
    with open(template_file, 'r', encoding='utf-8') as f:
        return f.read()
    
def fill_data_to_template(config, template_name: str) -> str:
    """Заполняет шаблон данными из JSON файла"""
    content = get_template_content(config, template_name)
    
    # Загружаем данные из JSON файла
    data = load_template_data(template_name)
    
    if not data:
        print(f"⚠️ No data file found for template: {template_name}")
        return content
    
    # Заменяем все плейсхолдеры в формате {{ variable }}
    filled_content = content
    for key, value in data.items():
        placeholder = r'{{\s*' + re.escape(key) + r'\s*}}'
        filled_content = re.sub(placeholder, str(value), filled_content)
    
    return filled_content

def load_template_data(template_name: str) -> dict:
    """Загружает данные для шаблона из JSON файла"""
    data_folder = pathlib.Path(__file__).parent / 'data' # Путь к папке с данными
    data_file = data_folder / f'{template_name}.json'
    
    if not data_file.exists():
        print(f"📁 Data file not found: {data_file}")
        return {}
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error loading data file {data_file}: {e}")
        return {}

def get_subject_from_template(config, template_name: str) -> str:
    """Возвращает тему из шаблона (title > h1 > template_name)"""
    content = get_template_content(config, template_name)
    # Приоритет 1: тег title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if title_match:
        subject = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        if subject:
            return subject
    
    # Приоритет 2: первый h1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if h1_match:
        subject = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
        if subject:
            return subject
    
    # Приоритет 3: имя шаблона как fallback
    return template_name.replace('_', ' ').title()
      
def get_text_message_from_template(content) -> str:
    """Возвращает текстовое содержимое шаблона по имени"""
    # Заменяем все теги, которые должны создавать новые строки
    replacements = [
        (r'</?(div|p|h[1-6])[^>]*>', '\n\n'),  # Блочные элементы - двойной перенос
        (r'<br[^>]*>', '\n'),                   # Переносы строк
        (r'</?(ul|ol)[^>]*>', '\n'),           # Списки
        (r'<li[^>]*>', '\n• '),                # Элементы списка
        (r'</li>', ''),
        (r'</tr>', '\n'),                      # Таблицы
        (r'</td>', '  '),
    ]
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    # Удаляем все остальные теги
    clean_text = re.sub(r'<[^>]+>', '', content)
    # Очистка и форматирование
    clean_text = re.sub(r'[ ]+', ' ', clean_text)  # Множественные пробелы
    clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)  # Нормализуем пустые строки
    clean_text = re.sub(r'^\s+|\s+$', '', clean_text)  # Обрезаем пробелы
    return clean_text

def get_action_from_user() -> str:
    action = input("""
    Select sending mode: 
    1 - One message
    2 - Many messages
    """)
    if action == '1':
        action = 'One message'
    elif action == '2':
        action = 'Many messages'
        
    return action
    
def get_mode_from_user() -> List:
    user_input = input("""
    Select the options:
    0 - not need
    1 - with CC
    2 - with BC
    3 - with attachments
    Enter all the numbers of the desired options, for example: 123
                """)
    mode = []
    if '1' in user_input:
        mode.append('cc')
    if '2' in user_input:
        mode.append('bcc')
    if '3' in user_input:
        mode.append('attachments')
        
    return mode

def get_template_from_user(config) -> str:
    templates_folder = config.get('EMAIL_TEMPLATES_FOLDER', 'messages_templates')
    email_templates = load_templates_from_folder(templates_folder)
    print("=== Select email template ===")
    for template in email_templates:
        print(template)
    template = input("Enter name of template: ")
    return template

def get_email_list_from_user() -> List:
    print("=== Enter email (empty for exit) ===")
    emails = []
    while True:
        email = input(f"Email {len(emails) + 1}: ").strip()
        if not email:
            break
        # Базовая проверка на наличие @
        if '@' in email and '.' in email.split('@')[-1]:
            emails.append(email)
            print(f"✅ Добавлен ({len(emails)})")
        else:
            print("❌ Неверный формат email")
    
    return emails

def get_attachments_urls_from_user() -> List:
    """Простой ввод путей к файлам"""
    attachments = []
    while True:
        path = input("Введите путь к файлу (Enter для завершения): ").strip()
        if not path:
            break
        attachments.append(path)

    return attachments
