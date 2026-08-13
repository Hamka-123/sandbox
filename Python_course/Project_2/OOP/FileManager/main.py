import pathlib
from class_file_manager import FileManager

file_manager = FileManager()
ROOT_TEST_FOLDER = pathlib.Path(__file__).parent / "Test_files"

USER_MENU = """
Please choose an option:
0. Exit
1. Create a new file
2. Create a new folder
3. Get file information by path
4. Get folder information by path
5. List files and folders in a directory
6. Copy a file or folder
7. Move a file or folder
8. Delete a file or folder
"""

while True:
    print(USER_MENU)
    choice = input("Enter your choice (1-8): ")
    match choice:
        case '0':
            print("Exiting the File Manager. Goodbye!")
            break

        case '1':
            new_file_name = input("Enter the file name: ")
            success = file_manager.create_file(ROOT_TEST_FOLDER, new_file_name, 2.5, 644, "2024-06-15", "txt")
            if success:
                # Создаем временный объект для отображения информации
                print(file_manager.get_recent_file_info(ROOT_TEST_FOLDER, new_file_name, "txt"))
            else:
                print("Failed to create file")

        case '2':
            new_folder_name = input("Enter the folder name: ")
            success = file_manager.create_folder(ROOT_TEST_FOLDER, new_folder_name, 0, 755, "2024-06-15")
            if success:
                # Создаем временный объект для отображения информации
                print(file_manager.get_recent_folder_info(ROOT_TEST_FOLDER, new_folder_name))
            else:
                print("Failed to create folder")

        case '3':
            file_path = pathlib.Path(input("Enter the file path: "))
            print(file_manager.get_file_info_by_path(file_path))

        case '4':
            folder_path = pathlib.Path(input("Enter the folder path: "))
            print(file_manager.get_folder_info_by_path(folder_path))

        case '5':
            dir_path_input = input("Enter the directory path (or press Enter for Test_files): ")
            dir_path = pathlib.Path(dir_path_input) if dir_path_input else ROOT_TEST_FOLDER
            items = file_manager.list_directory(dir_path)
            print("Items in directory:")
            for item in items:
                print(f"  - {item}")
        case '6':
            source_path = pathlib.Path(input("Enter the source path: "))
            destination_path = pathlib.Path(input("Enter the destination path: "))
            success = file_manager.copy_file_system_entity(source_path, destination_path)
            if success:
                print(f"Copied '{source_path}' to '{destination_path}' successfully.")
            else:
                print(f"Failed to copy '{source_path}' to '{destination_path}'.")

        case '7':
            source_path = pathlib.Path(input("Enter the source path: "))
            destination_path = pathlib.Path(input("Enter the destination path: "))
            success = file_manager.move_file_system_entity(source_path, destination_path)
            if success:
                print(f"Moved '{source_path}' to '{destination_path}' successfully.")
            else:
                print(f"Failed to move '{source_path}' to '{destination_path}'.")

        case '8':
            target_path = pathlib.Path(input("Enter the target path: "))
            success = file_manager.delete_file_system_entity(target_path)
            if success:
                print(f"Deleted '{target_path}' successfully.")
            else:
                print(f"Failed to delete '{target_path}'.")

        case _:
            print("Invalid choice. Please try again.")