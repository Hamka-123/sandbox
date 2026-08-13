# Что будет, если в декораторе не вернуть wrapper?
def bad_decorator(func):
    def wrapper():
        print("До вызова функции")
        func()
        print("После вызова функции")
    # ЗАБЫЛИ return wrapper!  ← КРИТИЧЕСКАЯ ОШИБКА

@bad_decorator
def hello():
    print("Hello World!")
    
print(hello())