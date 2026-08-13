'''
| Функция                                            | Что делает                                                        | Пример                                              |
| -------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------- |
| `shutil.copy(src, dst)`                            | Копирует файл `src` в `dst` (сохраняет содержимое, не метаданные) | `shutil.copy("file.txt", "backup.txt")`             |
| `shutil.copy2(src, dst)`                           | Копирует файл вместе с метаданными (дата создания, права доступа) | `shutil.copy2("file.txt", "backup.txt")`            |
| `shutil.copytree(src, dst)`                        | Рекурсивно копирует папку со всем содержимым                      | `shutil.copytree("my_folder", "backup_folder")`     |
| `shutil.rmtree(path)`                              | Рекурсивно удаляет папку и всё её содержимое                      | `shutil.rmtree("old_folder")`                       |
| `shutil.move(src, dst)`                            | Перемещает файл или папку                                         | `shutil.move("file.txt", "archive/file.txt")`       |
| `shutil.which(cmd)`                                | Находит путь к исполняемому файлу (как `which` в Linux)           | `shutil.which("python")`                            |
| `shutil.disk_usage(path)`                          | Возвращает информацию о диске: total, used, free                  | `shutil.disk_usage("/")`                            |
| `shutil.make_archive(base_name, format, root_dir)` | Создаёт архив (zip, tar и др.)                                    | `shutil.make_archive("backup", "zip", "my_folder")` |
| `shutil.unpack_archive(filename, extract_dir)`     | Распаковывает архив                                               | `shutil.unpack_archive("backup.zip", "restore")`    |

'''
import pathlib
import shutil

ROOT_FOLDER = pathlib.Path(__file__).parent
SRC_FOLDER = ROOT_FOLDER.joinpath('src')
DST_FOLDER = ROOT_FOLDER.joinpath('dst')

#copy files
shutil.copy(SRC_FOLDER.joinpath('test.txt'), DST_FOLDER)

shutil.copy(
    src = SRC_FOLDER.joinpath('test.txt'),
    dst = DST_FOLDER.joinpath('test2.txt')
    )

#copy folders with files and folders
shutil.copytree(SRC_FOLDER, DST_FOLDER, dirs_exist_ok=True)
#delete folders with files and folders

#TODO: shutil practice all methods
print(shutil.which('Python3'))

print(shutil.disk_usage('/'))

print(__name__)


