'''
Classes:
- Cart
- Product
- Customer

Tasks:
Customer class
    - add product to customer cart
    - show
    - remove
    - change quantity
    - get total

Product
    - DO DO ?
    - change_prise - ?
    
Cart
    - add / remove / change product
    - TO DO - ?


Shop
    Multiple customers
    Product stock (add products, remove ...)


'''
from shop import Shop

shop = Shop()

a = shop.add_product("A", 20.0, 5)
b = shop.add_product("B", 25.0, 3)
c = shop.add_product("C", 30.0, 2)
shop.add_product("D", 2.0, 100)
shop.add_product("E", 6.0, 8)

d = shop.get_product_by_name("D")
print(d)


print(shop.products)
shop.change_product_price(a, 50)
print("-"*20)
print(shop.products)

alina = shop.add_customer('Alina')
customer2 = shop.add_customer('Bob')
print(shop.customers)

alina.add_product_to_cart(a,1,shop)
alina.add_product_to_cart(b, 2, shop)
customer2.add_product_to_cart(d, 10, shop)
print(alina.show_cart())

alina.remove_product_from_cart(a)
print(alina.show_cart())

alina.change_quantity(b, 5)
alina.add_product_to_cart(a,1,shop)
print(alina.show_cart())
print(alina.get_cart_total())

shop.remove_product(d)
d = shop.get_product_by_name("D")
print(d)



