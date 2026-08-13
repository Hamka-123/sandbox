
class User:
    __id = 0
    name: str
    accounts:list
    
    def __init__(self, name):
        User.__id += 1
        self.id = User.__id
        self.name = name
        self.accounts = []
    
    def add_account(self, account_obj):
        self.accounts.append(account_obj)
        
    def add_new_account(self, balance):
        self.accounts.append(Account(self,balance))
        return self
        
    def remove_account(self, account_obj):
        self.accounts.remove(account_obj)
        
    def increase_account(self, account_number, amount):
        #get acc by number
        acc = None
        for ac in self.accounts:
            if ac.number == account_number: 
                acc = ac
                break
        #call acc method increase_balance
    
        if acc is None:
            print(f"Аккаунт {account_number} не найден")
            return None
        
        # Проверка принадлежит ли счет пользователю
        if acc.maintainer != self:
            print(f"Аккаунт {account_number} не принадлежит {self.name}")
            return None
        
        # Вызов метода увеличения баланса
        acc.increase_balance(amount)
        return acc.balance  # Используем геттер вместо прямого доступа
        
    def __repr__(self):
        return(f"""
              id пользователя: {self.id}
              Имя пользователя: {self.name}
              Счета: {self.accounts}
              """)
    
class Account:
    __acc_number = 100000000
    __maintainer:User
    __balance:float
    
    def __init__(self, maintainer='Bank', balance=0.0):
        Account.__acc_number += 1
        self.number = Account.__acc_number
        self.__maintainer = maintainer
        self.__balance = float(balance) if balance else 0.0
    
    @property
    def maintainer(self):
        return self.__maintainer
    
    @maintainer.setter
    def maintainer(self, user):
        if isinstance(user, User):
            self.__maintainer = user
        else:
            print(f"Ошибка: ожидается объект User, получен {type(user)}")
        
    @property
    def balance(self):
        return self.__balance
    
    def increase_balance(self, amount):
        self.__balance += float(amount)
        
    def decrease_balance(self, amount):
        if amount < self.__balance:
            self.__balance -= float(amount)
            return True
        else: return False
        
    def send_money(self, account_to, amount):
        if self.__balance >= amount:
            if self.decrease_balance(amount):
                account_to.increase_balance(amount)
                return True
            return False

    def __repr__(self):
        return(f"""
                _________________
                Счёт номер: {self.__acc_number}
                Баланс: {self.balance}
                Владелец: {self.maintainer}
              """) 
            
        

user1 = User('Alina')
user2 = User('Kira')

ac1 = Account()
ac2 = Account(user2, 50)
ac3 = Account()

user1.add_account(ac1)
ac1.maintainer = user1

user1.add_account(ac3)
ac3.maintainer = user1

ac4 = user1.add_new_account(500)
print(ac4)

user2.add_account(ac2)

ac1.increase_balance(200)
ac1.decrease_balance(100)
#user1.remove_account(ac1)
ac1.send_money(ac2, 50)   

user1.increase_account(ac1.number, 30)
print(ac1)
user1.increase_account(ac2.number, 30)
 
print(user1)

#print(dir(Account))
#print(dir(ac1))

ac1.__balance = 40
print(ac1.__balance) #40 !!!

print(ac1.__dict__)
print(user1.__dict__)