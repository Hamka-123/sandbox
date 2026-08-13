from uuid import UUID, uuid4
from cart import Cart

class Customer:
    def __init__(self, name):
        self.__id:UUID = uuid4()
        self._name:str = name
        self._cart:object = None 
        
    @property
    def id(self):
        return self.__id
    @property
    def name(self):
        return self._name
    @property
    def cart(self):
        return self._cart

    def add_product_to_cart(self, product, quantity=1, shop=None):
        """Добавить товар в корзину покупателю"""
        if self._cart is None:
            self._cart = Cart(self)
        # проверяем доступность товара
        if shop and not self._check_availability(product, quantity, shop):
            return False
        # Добавляем в корзину
        return self._cart.add_product(product, quantity)
    
    def _check_availability(self, product, quantity, shop):
        """Проверить доступно ли достаточное количество товара"""
        shop_product = shop.products.get(product.id)
        if not shop_product:
            print(f"❌ Товар {product.name} не найден в магазине")
            return False
        
        if shop_product.quantity < quantity:
            print(f"❌ Недостаточно товара {product.name}. Доступно: {shop_product.quantity}, запрошено: {quantity}")
            return False
        
        return True   
    
    def show_cart(self):
        """Показать корзину и её содержимое"""
        if self._cart is None:
            return "Cart is empty"
        
        cart_info = f"Cart N {self.cart.id}\n"
        if self.cart.products:
            product_names = self.cart.get_product_names()
            cart_info += "Products:\n" + "\n".join(f"  - {name}" for name in product_names)
            cart_info += f"\nTotal: ${self.cart.get_total()}"
        else:
            cart_info += "Cart is empty"
        
        return cart_info
    
    def get_cart_total(self):
        """Получить сумму к оплате"""
        if self._cart is None:
            return 0
        return self._cart.get_total()
    
    def remove_product_from_cart(self, product):
        """Удалить товар из корзины"""
        if self._cart is not None:
            return self._cart.remove_product(product)
        return False
    
    def change_quantity(self, product, new_quantity):
        """Изменить количество товара в корзине"""
        if self._cart is not None:
            return self._cart.change_quantity(product, new_quantity)
        return False
    
    def __repr__(self):
        cart_status = "has cart" if self._cart else "no cart"
        return f"Customer(name='{self.name}', {cart_status})"
    