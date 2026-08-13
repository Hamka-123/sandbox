
from class_file_system_entity import FileSystemEntity
import pathlib

class File(FileSystemEntity):
    extension:str
    path:pathlib.Path
    
    def __init__(self):
        super().__init__()
        self.extension = ""
        
    def create(self, path:pathlib.Path, name:str, size:float, permissions:int, date_created:str, extension:str):
        self.name = name
        self.size = size
        self.permissions = permissions
        self.date_created = date_created
        self.extension = extension
        self.path = path

        full_path = self.get_full_path()
        with open(full_path, 'w') as f:
            f.write("")  # создаем пустой файл


    def get_full_path(self) -> pathlib.Path:
        full_path = self.path.joinpath(f"{self.name}.{self.extension}")
        return full_path
    
    def get_file_info(self) -> str:
        info = f"""File Information:
                Name: {self.name},
                File path: {self.get_full_path()}, 
                Size: {self.size} MB,
                Permissions: {self.permissions}, 
                Date Created: {self.date_created}, 
                Extension: {self.extension}
                """
        return info
    
    @classmethod
    def from_path(cls, file_path: pathlib.Path) -> 'File':
        """Создает объект File из реального файла по пути"""
        file = cls()
        if file_path.exists() and file_path.is_file():
            stat = file_path.stat()
            file.path = file_path.parent
            file.name = file_path.stem
            file.extension = file_path.suffix[1:] if file_path.suffix else ""
            file.size = stat.st_size / (1024 * 1024)  # размер в MB
            file.permissions = stat.st_mode & 0o777
            file.date_created = stat.st_ctime
            return file
        return file  # возвращаем пустой объект если файл не найден
    
        