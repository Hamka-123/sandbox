from file_system_manager import FileSystemManager


fsManager = FileSystemManager()

# 
p = r'/Users/alinababenko/Documents/Israel_course/DevOps/Python_course/Project_2'
print(fsManager.child_names(p))


print(type(fsManager))