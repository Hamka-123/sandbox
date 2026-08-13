import pathlib


class FileSystemManager:
    
    def __init__(self):
        self.current_folder:str
        pass
    
    def child_names(self, abs_path) -> list[str]:
        res:list
        # Create folderEntry
        folder = FolderEntry(abs_path)
        
        # call children -> get names only
        res = [nam.name for nam in folder.children(abs_path)]
        # pathlib.Path().name
        
        
        return res    
    
    def child_entrees(self, abs_path) -> list[FileSystemEntry]:
        
        # Create folderEntry
        folder = FolderEntry(abs_path)
        
        # call children  -> entrees
        folder_content = folder.children(abs_path)
        
        
        
        return folder_content
    
    def get_current_folder(self) -> str:       
        
        return # TO DO   
      
    def set_current_folder(self) -> str:
        self.current_folder = self.get_current_folder()        
        return    
    
    
    pass

class FileSystemEntry:
    
    # Properties
    def __init__(self, name):
        self.size:float
        self.name = name
        self.permissions:int
        self.parent_abs_path:str
        self.date_creation:str
        self.date_last_change:str
        self.date_last_access:str
        
        
        pass
    
    # Methods
    
    def create(self, full_abs_path:str):
        # create
        
        # log
        
        
        pass
    
    def delete(self, full_abs_path:str):
        # create
        
        # log
        
        
        pass
    
    
    def exists(self, full_abs_path:str):
        
        pass
    
    def search(self, full_abs_path:str):
        
        pass
    
    pass


class FileEntry(FileSystemEntry):
    
    def __init__(self, name):
        super().__init__(name)
    
    pass


class FolderEntry(FileSystemEntry):
    
    def __init__(self, name):
        super().__init__(name)
        
        
    def children(self, full_abs_path:str, subfolders:bool | None = False) -> list[FileSystemEntry]:
        res:list
        if not subfolders:
            res = list(pathlib.Path(full_abs_path).iterdir())
        else:
            # TO DO recursive ...
            
            pass
        
        return  res
    
    
    pass


#  utility classes
class Recycler:
    # keep removed FS  entrees
    
    
    pass


class FsLogger:
    
    
    pass