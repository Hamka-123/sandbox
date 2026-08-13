from uuid import UUID, uuid4
from typing import List, Tuple

class Cart:
    def __init__(self, customer):
        self.__id = uuid4()
        self._customer:object = customer
        self._products: List[Tuple[object, int]] = []  # [(product, quantity), ...]
    
    @property
    def id(self):
        return self.__id
    
    @property
    def customer(self):
        return self._customer
    
    @property
    def products(self):
        return self._products
    
    def add_product(self, product, quantity=1):
        """Добавить продукт в корзину"""
        # Ищем продукт в корзине
        for i, (cart_product, cart_quantity) in enumerate(self._products):
            if cart_product.id == product.id:
                # Если нашли - увеличиваем количество
                self._products[i] = (cart_product, cart_quantity + quantity)
                return True
        
        # Если не нашли - добавляем новый
        self._products.append((product, quantity))
        return True
    
    def remove_product(self, product):
        """Удалить продукт из корзины полностью"""
        for i, (cart_product, cart_quantity) in enumerate(self._products):
            if cart_product.id == product.id:
                self._products.pop(i)
                return True
        return False
    
    def change_quantity(self, product, new_quantity):
        """Изменить количество продукта в корзине"""
        for i, (cart_product, cart_quantity) in enumerate(self._products):
            if cart_product.id == product.id:
                if new_quantity > 0:
                    self._products[i] = (cart_product, new_quantity)
                    return True
                else:
                    # Если количество 0 - удаляем продукт
                    self._products.pop(i)
                    return True
        return False
    
    def get_total(self):
        """Общая стоимость корзины"""
        total = 0
        for product, quantity in self._products:
            total += product.price * quantity
        return total
    
    def get_product_names(self):
        """Список продуктов с количеством и ценой"""
        names = []
        for product, quantity in self._products:
            names.append(f"{product.name} x{quantity} (${product.price} each)")
        return names
    
    def __repr__(self):
        if not self._products:
            return f"Cart(id={self.id}, empty)"
        
        total_items = sum(quantity for _, quantity in self._products)
        total_price = self.get_total()
        return f"Cart(id={self.id}, {total_items} items, total: ${total_price})"