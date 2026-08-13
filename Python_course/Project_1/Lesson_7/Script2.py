import pathlib #command + . -> Добавить импорт пакета
#pathlib - модуль для работы с путями


FILE_NAME = 'Script1.txt'
ACCESS_MODE = 'r' # r - read mode
HELP_TEXT ='''
Существует четыре различных способа (режима) открытия файла:
"r"- Read - Значение по умолчанию. Открывает файл для чтения, ошибка, если файл не существует
"a"- Добавить - открывает файл для добавления, создает файл, если он не существует
"w"- Запись - открывает файл для записи, создает файл, если он не существует
"x"- Создать - Создает указанный файл, возвращает ошибку, если файл существует.
Кроме того, вы можете указать, должен ли файл обрабатываться в двоичном или текстовом режиме.
"t"- Текст - Значение по умолчанию. Текстовый режим
"b"- Двоичный - Двоичный режим (например, изображения)

    #f - file object
    #w - write mode
    # The file is created if it does not exist
    # The file is overwritten if it exists
    # Writing to the file
'''
print(__file__) #absolute path to the current script
CURRENT_DIR = pathlib.Path(__file__).parent #absolute path to the current directory
FILE_PATH = CURRENT_DIR.joinpath("data_files",FILE_NAME) #absolute path to the file

with open(FILE_PATH, ACCESS_MODE) as f:
        #file_data = f.read() # Reading the file - to string
        file_data = f.readline() # read single line - to string
        file_data = f.readline() # read single line - to string
        file_data = f.readlines() # read all lines - to list[str]
        f.seek(0) # move the cursor to the beginning of the file
        f.truncate() # delete the file content
        f.flush() # flush the file content
        
        
print(file_data)

