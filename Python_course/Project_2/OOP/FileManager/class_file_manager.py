from class_file import File
from class_folder import Folder
from class_my_logger import MyLogger
import pathlib

class FileManager:
    def __init__(self):
        log_path = pathlib.Path(__file__).parent / "file_manager.log"
        self.logger = MyLogger(log_path)

    def create_file(self, path: pathlib.Path, name: str, size: float, permissions: int, date_created: str, extension: str) -> bool:
        """Создает файл и возвращает успех/неудачу, а не объект"""
        file = File()
        file.create(path, name, size, permissions, date_created, extension)
        
        file_path = path / f"{name}.{extension}"
        if file_path.exists():
            self.logger.info(f"File '{file_path}' created successfully.")
            return True
        else:
            self.logger.error(f"Failed to create file '{file_path}'.")
            return False

    def create_folder(self, path: pathlib.Path, name: str, size: float, permissions: int, date_created: str) -> bool:
        """Создает папку и возвращает успех/неудачу, а не объект"""
        folder = Folder()
        folder.create(path, name, size, permissions, date_created)
        
        folder_path = path / name
        if folder_path.exists():
            self.logger.info(f"Folder '{folder_path}' created successfully.")
            return True
        else:
            self.logger.error(f"Failed to create folder '{folder_path}'.")
            return False

    def get_file_info_by_path(self, file_path: pathlib.Path) -> str:
        """Получает информацию о файле по пути (создает временный объект)"""
        file_obj = File.from_path(file_path)
        if file_obj and file_obj.name:
            return file_obj.get_file_info()
        else:
            error_msg = f"File not found: {file_path}"
            self.logger.error(error_msg)
            return error_msg

    def get_folder_info_by_path(self, folder_path: pathlib.Path) -> str:
        """Получает информацию о папке по пути (создает временный объект)"""
        folder_obj = Folder.from_path(folder_path)
        if folder_obj and folder_obj.name:
            return folder_obj.get_folder_info()
        else:
            error_msg = f"Folder not found: {folder_path}"
            self.logger.error(error_msg)
            return error_msg

    def get_recent_file_info(self, path: pathlib.Path, name: str, extension: str) -> str:
        """Получает информацию о только что созданном файле"""
        file_path = path / f"{name}.{extension}"
        return self.get_file_info_by_path(file_path)

    def get_recent_folder_info(self, path: pathlib.Path, name: str) -> str:
        """Получает информацию о только что созданной папке"""
        folder_path = path / name
        return self.get_folder_info_by_path(folder_path)

    def list_directory(self, dir_path: pathlib.Path) -> list:
        """Список файлов и папок в директории"""
        try:
            if dir_path.exists() and dir_path.is_dir():
                items = []
                for item in dir_path.iterdir():
                    items.append(item.name)
                return items
            else:
                return [f"Directory not found: {dir_path}"]
        except Exception as e:
            return [f"Error listing directory: {e}"]
        
    def copy_file_system_entity(self, source_path: pathlib.Path, destination_path: pathlib.Path) -> bool:
        """Копирует файл или папку из source_path в destination_path"""
        try:
            if source_path.exists():
                if source_path.is_file():
                    dest_file = destination_path / source_path.name
                    with open(source_path, 'rb') as src_f, open(dest_file, 'wb') as dest_f:
                        dest_f.write(src_f.read())
                elif source_path.is_dir():
                    dest_folder = destination_path / source_path.name
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    for item in source_path.iterdir():
                        self.copy_file_system_entity(item, dest_folder)
                self.logger.info(f"Copied '{source_path}' to '{destination_path}' successfully.")
                return True
            else:
                self.logger.error(f"Source path not found: {source_path}")
                return False
        except Exception as e:
            self.logger.error(f"Error copying '{source_path}' to '{destination_path}': {e}")
            return False
        
    def move_file_system_entity(self, source_path: pathlib.Path, destination_path: pathlib.Path) -> bool:
        """Перемещает файл или папку из source_path в destination_path"""
        try:
            if self.copy_file_system_entity(source_path, destination_path):
                if source_path.is_file():
                    source_path.unlink()
                elif source_path.is_dir():
                    for item in source_path.iterdir():
                        if item.is_dir():
                            item.rmdir()
                        else:
                            item.unlink()
                    source_path.rmdir()
                self.logger.info(f"Moved '{source_path}' to '{destination_path}' successfully.")
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Error moving '{source_path}' to '{destination_path}': {e}")
            return False
        
    def delete_file_system_entity(self, target_path: pathlib.Path) -> bool:
        """Удаляет файл или папку по пути target_path"""
        try:
            if target_path.exists():
                if target_path.is_file():
                    target_path.unlink()
                elif target_path.is_dir():
                    for item in target_path.iterdir():
                        if item.is_dir():
                            item.rmdir()
                        else:
                            item.unlink()
                    target_path.rmdir()
                self.logger.info(f"Deleted '{target_path}' successfully.")
                return True
            else:
                self.logger.error(f"Target path not found: {target_path}")
                return False
        except Exception as e:
            self.logger.error(f"Error deleting '{target_path}': {e}")
            return False