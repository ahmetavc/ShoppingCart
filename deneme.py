food = Category('food')
home = Category('home')
vegetable = Category('vegetable', food)

apple = Product('apple', 100.0, food)
almond = Product('almond', 50.0,.food)
chair = Product('chair', 100.0, home)
tomato = Product('tomato', 100.0, vegetable)

cart = ShoppingCart()
cart.addItem(apple, 3)
cart.addItem(almond, 1)
cart.addItem(chair, 2)
cart.addItem(tomato, 1)

campaign1 = Campaign(food, 25.0, 1, DiscountType.Rate)
campaign2 = Campaign(home, 50.0, 3, DiscountType.Rate)
campaign3 = Campaign(food, 12, 1, DiscountType.Amount)
campaign4 = Campaign(home, 10, 3, DiscountType.Amount)

coupon1 = Coupon(100.0, 10.0, DiscountType.Rate)
coupon2 = Coupon(1000.0, 10.0, DiscountType.Rate)
coupon3 = Coupon(100.0, 100.0, DiscountType.Amount)
coupon4 = Coupon(1000.0, 100.0, DiscountType.Amount)



