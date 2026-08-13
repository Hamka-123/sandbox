import os
#https://www.w3schools.com/python/module_os.asp#gsc.tab=0

import pathlib
#https://www.geeksforgeeks.org/python/pathlib-module-in-python/
'''
| Операция / Задача                      | os                                                                       | glob                                                       | pathlib                                            |
| -------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------- | -------------------------------------------------- |
| Получить список всех элементов в папке | `os.listdir(path)`                                                       | —                                                          | `Path(path).iterdir()`                             |
| Получить список только файлов          | `[f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]` | `[f for f in glob.glob(path + "/*") if os.path.isfile(f)]` | `[f for f in Path(path).iterdir() if f.is_file()]` |
| Получить список файлов по шаблону      | `[f for f in os.listdir(path) if fnmatch.fnmatch(f, "*.txt")]`           | `glob.glob(path + "/*.txt")`                               | `Path(path).glob("*.txt")`                         |
| Рекурсивный поиск файлов               | —                                                                        | `glob.glob(path + "/**/*.txt", recursive=True)`            | `Path(path).rglob("*.txt")`                        |
| Проверка существования файла/папки     | `os.path.exists(path)`                                                   | —                                                          | `Path(path).exists()`                              |
| Проверка на файл                       | `os.path.isfile(path)`                                                   | —                                                          | `Path(path).is_file()`                             |
| Проверка на папку                      | `os.path.isdir(path)`                                                    | —                                                          | `Path(path).is_dir()`                              |
| Создать папку                          | `os.mkdir(path)` / `os.makedirs(path)`                                   | —                                                          | `Path(path).mkdir(parents=True, exist_ok=True)`    |
| Удалить файл                           | `os.remove(path)`                                                        | —                                                          | `Path(path).unlink()`                              |
| Удалить папку                          | `os.rmdir(path)` / `os.removedirs(path)`                                 | —                                                          | `Path(path).rmdir()`                               |
| Переименовать / переместить            | `os.rename(src, dst)` / `os.replace(src, dst)`                           | —                                                          | `Path(src).rename(dst)`                            |
| Текущая рабочая директория             | `os.getcwd()`                                                            | —                                                          | `Path.cwd()`                                       |
| Сменить рабочую директорию             | `os.chdir(path)`                                                         | —                                                          | `Path().chdir()` (через os.chdir)                  |

'''

#TODO:  🔹 Работа с файлами и папками – задачи для практики

#✅TODO: 1. Прочитать текстовый файл и подсчитать:
#    - количество строк
#    - количество слов
#    - количество символов
DATA_FOLDER = pathlib.Path(__file__).parent.joinpath("datafiles")
SOURCE_FILE = DATA_FOLDER.joinpath("users.csv")

with open(SOURCE_FILE, 'r') as f: 
    file_data_string = f.read().strip()
    pass

list_lines = file_data_string.split('\n')
count_lines = len(list_lines)
count_words = 0
count_symbols = 0
for i in list_lines:
    count_words += len(i.split(',') )
    count_symbols += len(i.replace(',',''))
    
print(count_lines)
print(count_words)
print(count_symbols)

#✅TODO: 2. Записать список чисел в файл, а затем прочитать его обратно в список
DATA_FOLDER = pathlib.Path(__file__).parent.joinpath("datafiles")
SOURCE_FILE = DATA_FOLDER.joinpath("numbers.txt")

data = [1,3,5,6,3,6,8,9,4,2,10]

with open(SOURCE_FILE, 'w') as f: 
    f.write(str(data) + '\n')
    pass

with open(SOURCE_FILE, 'r') as f: 
    file_data_string = f.read().strip()
    pass

print(file_data_string)
file_data_string = file_data_string.strip("[]")
List3 = [int(x.strip()) for x in file_data_string.split(",")]
print('-'*100, '\n', List3)

#✅TODO: 3. Создать папку, если она не существует
FOLDER1_PATH = pathlib.Path(__file__).parent.parent.joinpath("test_folder1")
FOLDER2_PATH = pathlib.Path(__file__).parent.parent.joinpath("test_folder2")

print(FOLDER1_PATH.exists(), '\n', os.path.exists(FOLDER2_PATH))

if FOLDER1_PATH.exists() == False:
    os.mkdir(FOLDER1_PATH)
if FOLDER2_PATH.exists() == False:
    os.mkdir(FOLDER2_PATH)

print(FOLDER1_PATH.exists(), '\n', os.path.exists(FOLDER2_PATH))


#✅TODO: 4. Получить список всех файлов в папке (не включая подпапки)
START_FOLDER = pathlib.Path.cwd() #root
#START_FOLDER = os.getcwd() #root
print(START_FOLDER)
# os.listdir() 
print(os.listdir(START_FOLDER))

# os.scandir()
print(os.scandir(START_FOLDER))

# glob.glob() https://docs.python.org/3/library/glob.html

# pathlib.Path
print(pathlib.Path(START_FOLDER).iterdir())

#✅TODO: 5. Получить список всех файлов и подпапок в папке
TARGET_FILE = pathlib.Path.cwd().joinpath('Project_2')
items = TARGET_FILE.iterdir()
#print(*items)

#✅TODO: 6. Проверить, существует ли файл или папка по пути
PATH =  pathlib.Path.cwd().joinpath('Project_2','TO_DO')
print(PATH.exists())

#✅TODO: 7. Узнать размер файла в байтах
PATH =  pathlib.Path.cwd().joinpath('Project_2','TO_DO','tt.log')
if PATH.exists:
    size = PATH.lstat().st_size
    size = PATH.stat().st_size
    print(size)

#✅TODO:  8. Переименовать файл или папку
'''
PATH =  pathlib.Path.cwd().joinpath('Project_2','TO_DO','test_folder3')
new_path = PATH.parent / 'test_folder4'
PATH.rename(new_path)
'''

#✅TODO: 9. Удалить файл
'''
PATH2 = pathlib.Path.cwd().joinpath('Project_2','TO_DO','to_delete.py')
PATH2.unlink()
print(PATH2.exists())
'''

#✅TODO: 10. Удалить пустую папку
'''
PATH3 = pathlib.Path.cwd().joinpath('Project_2','TO_DO','test_folder4')
if not any(PATH3.iterdir()):
    PATH3.rmdir()
'''

#TODO: 11. Рекурсивно удалить папку с содержимым

#✅TODO: 12. Соединить несколько частей пути в один путь (кроссплатформенно)
PART1 = pathlib.Path.cwd().joinpath('Project_2','TO_DO')
PART2 = 'test_folder2'
PATH4 = PART1.joinpath(PART2)
print(PATH4)

# Просто и эффективно
SEPARATOR = os.path.sep
print(f"Разделитель для текущей ОС: '{SEPARATOR}'")

# Пример использования
parts = ['home', 'user', 'file.txt']
path = SEPARATOR.join(parts)
print(f"Собранный путь: {path}")

#✅TODO: 13. Разделить путь на:
#     - директорию
#     - имя файла
#     - расширение файла
parts = path.split(SEPARATOR)
path_info = {
    'directory': SEPARATOR.join(parts[:-1]),
    'file_name': parts[-1].split('.')[:-1],
    'extension': parts[-1].split('.')[-1]
}
print(path_info.items())

#TODO: 14. Проверить, является ли путь файлом или папкой
PATH3 = pathlib.Path.cwd().joinpath('Project_2','TO_DO','test_folder4')
'''
#✅TODO: 15. Прочитать CSV-файл и преобразовать его в список списков

DATA_FOLDER = pathlib.Path(__file__).parent.joinpath("datafiles")
SOURCE_FILE = DATA_FOLDER.joinpath("users.csv")
with open(SOURCE_FILE) as f:
    string_from_file = f.read()
    pass

def convert_from_string_to_list_list_csv(file_data):
    return [line.strip().split(',') for line in file_data.strip().split('\n')]

List1 = convert_from_string_to_list_list_csv(string_from_file)
#print(List1)


#✅TODO: 16. Прочитать CSV-файл и преобразовать в список словарей по заголовкам
DATA_FOLDER = pathlib.Path(__file__).parent.joinpath("datafiles")
SOURCE_FILE = DATA_FOLDER.joinpath("users.csv")
with open(SOURCE_FILE) as f:
    string_from_file = f.read()
    pass

List1 = convert_from_string_to_list_list_csv(string_from_file)
def convert_list_to_list_dict(list_data):
    keys = list_data[0]
    return [{k: v for k, v in zip(keys, row)} for row in list_data[1:]]

List2 = convert_list_to_list_dict(List1)
#print('-'*100, '\n', List2)


#✅TODO: 17. Записать список словарей в CSV-файл с заголовками
TARGET_FILE = DATA_FOLDER.joinpath("users_new.csv")
'''
#✅TODO: 18. Использовать pathlib для:
#     - работы с путями
#     - создания папок
#     - проверки существования файлов и папок
TARGET_FILE = pathlib.Path(__file__).parent.joinpath('datafiles')
if TARGET_FILE.exists():
    new_folder = TARGET_FILE.joinpath('new_dir')
    new_folder.mkdir(exist_ok=True)
    print(f"✅ Вложенная папка создана: {new_folder}")
    print(TARGET_FILE.joinpath('numbers.txt').exists())

#TODO: 19. Сравнить использование open() + read() и with open() для чтения файлов

#TODO: 20. Скопировать файл или папку в другую директорию (shutil)

#TODO: 21. Переместить файл или папку в другую директорию (shutil)

#TODO: 22. Получить абсолютный путь файла

#TODO: 23. Получить текущую рабочую директорию и сменить её

#TODO: 24. Создать временный файл или папку и работать с ним (tempfile)

#TODO: 25. Считать все строки файла, которые удовлетворяют определённому условию
#     (например, начинаются с определённого слова)

#TODO: 🔹 Расширенные задачи по работе с файлами и папками

#TODO: 1. Создать структуру папок "project/src/utils" с помощью pathlib
#TODO: 2. Получить список всех .txt файлов в папке и всех подпапках рекурсивно
#TODO: 3. Найти все файлы больше определённого размера (например, 1 МБ)
#TODO: 4. Переместить все .log файлы из одной папки в другую
#TODO: 5. Скопировать все изображения (.jpg, .png) из одной папки в backup-папку
#TODO: 6. Переименовать все файлы в папке, добавив префикс "new_"
#TODO: 7. Удалить все пустые подпапки внутри заданной директории
#TODO: 8. Прочитать все CSV-файлы в папке и объединить их в один список словарей
#TODO: 9. Создать резервную копию файла с добавлением текущей даты в имя
#TODO: 10. Разделить имя файла и расширение для всех файлов в папке
#TODO: 11. Проверить, какие файлы в папке изменялись за последние 7 дней
#TODO: 12. Создать текстовый файл и записать в него строки из списка
#TODO: 13. Прочитать файл построчно и сохранить только уникальные строки
#TODO: 14. Считать все файлы в папке, у которых имя содержит определённое слово
#TODO: 15. Получить абсолютные пути всех файлов в папке и отсортировать по имени
#TODO: 16. Использовать pathlib для проверки: является ли путь файлом или папкой
#TODO: 17. Рекурсивно удалить папку и всё её содержимое
#TODO: 18. Найти все файлы с расширением .py и посчитать количество строк кода
#TODO: 19. Создать временную папку и файл внутри неё (tempfile)
#TODO: 20. Сравнить содержимое двух файлов на идентичность
#TODO: 21. Переименовать файлы с неправильными символами в имени на допустимые
#TODO: 22. Объединить содержимое нескольких текстовых файлов в один
#✅TODO: 23. Вывести все файлы, изменённые сегодня
import datetime

PATH5 = pathlib.Path.cwd().joinpath('Project_2')
today = datetime.datetime.now().date()

# Рекурсивный поиск во всех подпапках
today_list = [
    file for file in PATH5.rglob('*') 
    if file.is_file() and 
    datetime.datetime.fromtimestamp(file.stat().st_mtime).date() == today
]

print("📄 Файлы, измененные сегодня (рекурсивно):")
for file in today_list:
    mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
    print(f"  - {file.relative_to(PATH5)} ({mtime.strftime('%H:%M:%S')})")
    
WORKING_LOG = PATH5 / 'working_log'
# Создаем папку если не существует
if not WORKING_LOG.exists():
    WORKING_LOG.mkdir(parents=True, exist_ok=True)

# Создаем файл с сегодняшней датой
today = datetime.datetime.now().strftime('%Y-%m-%d')
log_file = WORKING_LOG / f'log_{today}.txt'

# Записываем в файл
log_file.write_text(f'Лог начат: {datetime.datetime.now()}\n')
print(f"✅ Лог-файл создан: {log_file}")
# Записываем список файлов в лог
with open(log_file, 'w', encoding='utf-8') as f:
    f.write(f"=== ФАЙЛЫ, ОТРЕДАКТИРОВАННЫЕ {today} ===\n\n")
    
    if today_list:
        for i, file in enumerate(today_list, 1):
            mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
            size = file.stat().st_size
            f.write(f"{i:2}. {file.name}\n")
            f.write(f"    Путь: {file.relative_to(PATH5)}\n")
            f.write(f"    Время изменения: {mtime.strftime('%H:%M:%S')}\n")
            f.write(f"    Размер: {size} байт\n")
            f.write(f"    Расширение: {file.suffix}\n\n")
    else:
        f.write("❌ Сегодня не было изменений файлов\n")
    

#TODO: 24. Скопировать структуру папок без файлов
#TODO: 25. Сжать папку в .zip и разархивировать обратно (shutil.make_archive / unpack_archive)