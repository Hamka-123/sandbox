from uuid import UUID, uuid4


class Product: 
    def __init__(self, name, price, quantity):
        self.__id:UUID = uuid4()
        self._name:str = name
        self._price:float = price
        self._quantity:int = quantity
        
    @property
    def id(self):
        return self.__id
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @property
    def quantity(self):
        return self._quantity
    
    @price.setter
    def price(self, price):
        """Установить новую цену на товар"""
        if price > 0:
            self._price = price
            return f"Новая цена товара {self.name} установлена {self.price}" if self._price == price else "Error"
        return "Ошибка: цена должна быть положительной"
    
    def __repr__(self):
        return f"Product: (name={self.name}, price={self.price}, quantity={self.quantity})"