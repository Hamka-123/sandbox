from class_file_system_entity import FileSystemEntity
import pathlib


class Folder(FileSystemEntity):
    path:pathlib.Path

    def __init__(self):
        super().__init__()

    def create(self, path: pathlib.Path, name: str, size: float, permissions: int, date_created: str):
        self.name = name
        self.size = size
        self.permissions = permissions
        self.date_created = date_created
        self.path = path / self.name
        
        self.path.mkdir(parents=True, exist_ok=True)
        
    def get_full_path(self) -> pathlib.Path:
        full_path = self.path.joinpath(f"{self.name}")
        return full_path
    
    def get_folder_info(self) -> str:
        info = f"""Folder Information:
                Name: {self.name},
                Folder path: {self.get_full_path()}, 
                Size: {self.size} MB,
                Permissions: {self.permissions}, 
                Date Created: {self.date_created}
                """
        return info 
    
    @classmethod
    def from_path(cls, folder_path: pathlib.Path) -> 'Folder':
        """Создает объект Folder из реальной папки по пути"""
        folder = cls()
        if folder_path.exists() and folder_path.is_dir():
            stat = folder_path.stat()
            folder.path = folder_path.parent
            folder.name = folder_path.name
            folder.size = 0  # размер папки сложно вычислить
            folder.permissions = stat.st_mode & 0o777
            folder.date_created = stat.st_ctime
            return folder
        return folder  # возвращаем пустой объект если папка не найдена
    