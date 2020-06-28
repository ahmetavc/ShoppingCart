from ShoppingCart import ShoppingCart

class DeliveryCostCalculator:

    def __init__(self, costPerDelivery: float, costPerProduct: float, fixedPrice: float) -> None:
        self.costPerDelivery = costPerDelivery
        self.costPerProduct = costPerProduct
        self.fixedPrice = fixedPrice

    def calculateFor(self, cart: ShoppingCart) -> float:
        # I took related categories as unique since they are distinct.    
        numberOfDeliveries = len(cart.categories.keys())
        numberOfProducts = 0

        # all products counts as unique since I assumed that product titles are unique
        for category in cart.categories:
            numberOfProducts += len(cart.categories[category]['products'])

        cart.deliveryCost = (self.costPerDelivery * numberOfDeliveries) + (self.costPerProduct * numberOfProducts) + self.fixedPrice

        return cart.deliveryCost