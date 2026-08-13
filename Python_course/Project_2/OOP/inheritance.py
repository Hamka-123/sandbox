#hierarchical inheritance
class Person:
    name:str
    age:int
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f"{Person.__name__}, {self.name=}, {self.age=} "
   

class Student(Person):
    course: str
    group: str

    def __init__(self, name, age, course, group):
        super().__init__(name, age)
        self.course = course
        self.group = group
        
    def __repr__(self):
        return super().__repr__() + f"{Student.__name__}, {self.course=}, {self.group=} "
    
    
class Employee(Person):
    salary:str
    position: str
    
    def __init__(self, name, age, salary, position):
        super().__init__(name, age)
        self.salary = salary
        self.position = position
        
    def __repr__(self):
        return super().__repr__() +  f"{Employee.__name__}, {self.salary=}, {self.position=} "
        
    
haim = Student('Haim', 20, 'Devops', 'DevOps_1')
print(haim)

print(Student.mro())

print(isinstance(haim, Person))
print(isinstance(haim, Employee))
print(isinstance(haim, Student))
'''
True
False
True
'''
print(Student.__bases__)
    
import torch

# Проверяем доступность CUDA
print(f"CUDA доступна: {torch.cuda.is_available()}")
print(f"Количество GPU: {torch.cuda.device_count()}")
print(f"Текущая GPU: {torch.cuda.current_device()}")
print(f"Название GPU: {torch.cuda.get_device_name(0)}")
