class FileSystemEntity:
    name:str
    size:float
    permissions:int
    date_created:str
    
    def __init__(self):
        self.name = ""
        self.size = 0.0
        self.permissions = 0
        self.date_created = ""
        
    