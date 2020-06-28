from Category import Category
from ShoppingCart import ShoppingCart
from Product import Product


print('LETS BEGIN')
food = Category('food')
home = Category('home')

apple = Product('apple', 100.0, food)
almond = Product('almond', 50.0, food)
chair = Product('chair', 100.0, home)
table = Product('table', 50.0, home) 

cart = ShoppingCart()

cart.addItem(apple, 3)
cart.addItem(almond, 1)
cart.addItem(chair, 5)
cart.addItem(table, 3)

print(cart.categories)


