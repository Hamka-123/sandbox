# read / write users.json
# CRUD operations:
## - Create 
## - Read 
## - Update 
## - Delete

# CLI - Command Line Interface

# GUI - Graphical User Interface (for future implementations !!!)

# ------------------------------------------------------------------------------------------------
# -- imports
# ------------------------------------------------------------------------------------------------
import json
import pathlib

# ------------------------------------------------------------------------------------------------
# -- configuration
# ------------------------------------------------------------------------------------------------
ROOT_FOLDER = pathlib.Path(__file__).parent
SOURCE_FILE = ROOT_FOLDER.joinpath("users.json")
DEFAULT_FIELDS = ["name", "age", "email"]  # Если файла нет, используем эти поля
# ------------------------------------------------------------------------------------------------
# -- functions
# ------------------------------------------------------------------------------------------------
def get_user_fields(file: pathlib.Path) -> list:
    """
    Получает список полей пользователей из JSON-файла.
    Если файл не существует или пустой — возвращает DEFAULT_FIELDS.

    Args:
        file (pathlib.Path): Путь к JSON-файлу.

    Returns:
        list: Список ключей (полей) для пользователя.
    """
    try:
        data = read(file)
        if data:
            return list(data[0].keys())
        else:
            return DEFAULT_FIELDS
    except FileNotFoundError:
        return DEFAULT_FIELDS


def input_user_data(fields: list, existing_data: dict = None) -> dict:
    """
    Запрашивает значения для всех полей пользователя.

    Args:
        fields (list): Список полей для запроса.
        existing_data (dict, optional): Существующие данные для Update. Defaults to None.

    Returns:
        dict: Словарь с данными пользователя.
    """
    user_data = {}
    for field in fields:
        default_value = existing_data.get(field) if existing_data else ""
        value = input(f"{field} [{default_value}]: ").strip()
        user_data[field] = value if value else default_value
    return user_data

def create(user: dict, file: pathlib.Path) -> str:
    """
    Добавляет нового пользователя в локальный JSON-файл.

    Args:
        user (dict): Словарь с данными пользователя.
        file (pathlib.Path): Путь к JSON-файлу.

    Returns:
        str: Сообщение об успешном добавлении.
    """
    try:
        data = read(file)  # читаем существующих пользователей
    except FileNotFoundError:
        data = []  # если файла нет, создаём новый список

    data.append(user)
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return f"Пользователь {user} добавлен"


def read(file: pathlib.Path) -> list:
    """
    Читает список пользователей из локального JSON-файла.

    Args:
        file (pathlib.Path): Путь к JSON-файлу.

    Returns:
        list: Список пользователей (каждый пользователь — словарь).
    """
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def update(username: str, new_data: dict, file: pathlib.Path) -> str:
    """
    Обновляет данные указанного пользователя.

    Args:
        username (str): Имя пользователя для обновления.
        new_data (dict): Словарь с новыми данными.
        file (pathlib.Path): Путь к JSON-файлу.

    Returns:
        str: Сообщение об успешном обновлении или ошибке.
    """
    data = read(file)
    for user in data:
        if user.get("name") == username:
            user.update(new_data)
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return f"У пользователя {username} обновлёны данные {new_data}"
    return f"Пользователь {username} не найден"


def delete(username: str, file: pathlib.Path) -> str:
    """
    Удаляет указанного пользователя из файла.

    Args:
        username (str): Имя пользователя для удаления.
        file (pathlib.Path): Путь к JSON-файлу.

    Returns:
        str: Сообщение об успешном удалении или ошибке.
    """
    data = read(file)
    new_data = [user for user in data if user.get("name") != username]

    if len(new_data) == len(data):
        return f"Пользователь {username} не найден"

    with open(file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    return f"Пользователь {username} удалён"


# ------------------------------------------------------------------------------------------------
# -- main
# ------------------------------------------------------------------------------------------------
print("=== User Management CLI ===")
print("Файл пользователей:", SOURCE_FILE)

while True:
    print("\nВыберите действие:")
    print("1 - Добавить пользователя (Create)")
    print("2 - Просмотреть всех пользователей (Read)")
    print("3 - Обновить пользователя (Update)")
    print("4 - Удалить пользователя (Delete)")
    print("5 - Выход")

    choice = input("Ваш выбор: ").strip()
    fields = get_user_fields(SOURCE_FILE)

    match choice:
        case "1":
            # Create
            user_data = input_user_data(fields)
            print(create(user_data, SOURCE_FILE))

        case "2":
            # Read
            try:
                users = read(SOURCE_FILE)
                if not users:
                    print("Список пользователей пуст.")
                else:
                    print("Список пользователей:")
                    for u in users:
                        print(u)
            except FileNotFoundError:
                print("Файл пользователей не найден.")

        case "3":
            # Update
            username_field = fields[0]  # считаем, что первое поле — идентификатор пользователя
            username = input(f"Введите {username_field} для обновления: ").strip()
            users = read(SOURCE_FILE)
            existing_user = next((u for u in users if u.get(username_field) == username), None)
            if not existing_user:
                print(f"Пользователь {username} не найден.")
                continue

            print("Введите новые данные (оставьте пустым, если не менять):")
            new_data = input_user_data(fields, existing_user)
            print(update(username, new_data, SOURCE_FILE))

        case "4":
            # Delete
            username_field = fields[0]
            username = input(f"Введите {username_field} для удаления: ").strip()
            print(delete(username, SOURCE_FILE))

        case "5":
            print("Выход из программы.")
            break

        case _:
            print("Некорректный выбор. Попробуйте снова.")
