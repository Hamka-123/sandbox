
#create class

class Person:
    #data - свойства
    class_description = 'Hello'
    name:str = 'NO_NAME'
    
    #methods - методы
    def __init__(self, name):
        self.name = name
        
    def tell_something(self):
        print('Say: ' + self.class_description)


p1 = Person("1")
p2 = Person("2")

p1.tell_something()
p2.tell_something()

#p1.class_description = 'aaaaa'
p2.class_description = 'bbbbb'
Person.class_description = 'ccccc'

print(Person.class_description)
#Person.tell_something("sdasd")

print(p1.class_description)
print(p2.class_description)

p1.aaa = 'aaa'
print(p1.aaa)

print(dir(p1))
'''
['__annotations__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'class_description', 'name', 'tell_something']
'''
print(dir(Person))

print(type(p1))

import sys

print(sys.getrefcount(p1))

