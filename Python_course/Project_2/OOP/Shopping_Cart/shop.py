from uuid import UUID
from customer import Customer
from product import Product

class Shop:
    def __init__(self):
        self.products: dict[UUID, Product] = {}
        self.customers: dict[UUID, Customer] = {}
    
    def add_product(self, name, price, quantity):
        """Добавить продукт в магазин"""
        new_product = Product(name, price, quantity)
        self.products[new_product.id] = new_product
        return new_product
    
    def get_product_by_name(self, name):
        """Найти продукт по имени"""
        for product in self.products.values():
            if product.name == name:
                return product
        return None
    
    def remove_product(self, product):
        """Удалить продукт из магазина"""
        if product.id in self.products.keys():
            self.products.pop(product.id)
    
    def change_product_price(self, product, new_price):
        """Изменить цену продукта в магазине"""
        if product.id in self.products:
            self.products[product.id].price = new_price
            return True
        return False
    
    def add_customer(self, name):
        """Добавить покупателя"""
        new_customer = Customer(name)
        self.customers[new_customer.id] = new_customer
        return new_customer
    
    def __repr__(self):
        return f"Shop(products: {len(self.products)}, customers: {len(self.customers)})"