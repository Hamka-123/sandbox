class Student:
    __counter = 0
    
    def __init__(self, first_name,last_name,email,gender,course,balance):
        #Create new object
        Student.__counter += 1
        self.id = Student.__counter
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.course = course
        self.balance = balance
        
    def __repr__(self):
        to_print = f"""
        {self.id = }
        {self.first_name = }
        {self.last_name = }
        {self.email = }
        {self.gender = }
        {self.course = }
        {self.balance = }
        """
        return to_print

    def get_full_name(self):
        return self.first_name +' '+ self.last_name
    
    def update_balance(self, amount):
        self.new_balance = float(self.balance) + amount
        return self.new_balance
    
#v2
class StudentV2:
    # Class fields:
    __counter = 0
    
    # Object fields
    id:int
    first_name:str
    last_name:str
    email:str
    gender:str
    course:str
    balance:float
    group:str
    
    def __init__(self, *props): # *args
        # Creating new object
        StudentV2.__counter += 1      
        self.id=StudentV2.__counter
        self.first_name = props[0]
        self.last_name = props[1]
        self.email = props[2]
        self.gender = props[3]
        self.course = props[4]
        self.balance = float(props[5]) if props[5] else 0
        self.group = props[6] if props[6] else None

    def __repr__(self):
        to_print = f"""
        {self.id = }
        {self.first_name = }
        {self.last_name = }
        {self.email = }
        {self.gender = }
        {self.course = }
        {self.balance = }
        {self.group = }
        """
        return to_print
    
    def change_fields(self, **kwprops):
        """
        Обновить поля в объекте StudentV2
        __________________________________
        first_name:str
        last_name:str
        email:str
        gender:str
        course:str
        balance:float
        group:str
        """
        for field, value in kwprops.items():
            if hasattr(self, field):
                if field == 'balance':
                    value = float(value)
                setattr(self, field, value)
        
    def check_balance(self):
        return "TRUE" if self.balance > 0 else "FALSE"