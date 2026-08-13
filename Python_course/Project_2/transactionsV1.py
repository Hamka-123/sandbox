def transactions():
    balance = 0
    
    def increment(amount):
            nonlocal balance
            balance += amount
            print(balance)
    def decrement(amount):
            nonlocal balance
            balance -= amount
            print(balance)
            
    def transact(amount):
        if amount >= 0:
            increment(amount)
        else:
            decrement(-amount) 
    return transact
    
account = transactions()

account(100) # -> print balance after increment
account(-50) # -> print balance after increment

'''
Проще:
def create():
    balance = 0
    def account(amount):
        nonlocal balance
        balance += amount
        return balance
    return account
    
account = create()
print(account(100))
print(account(-50))
'''