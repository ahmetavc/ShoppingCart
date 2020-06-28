class DeliveryCostCalculator:

    def __init__(self, costPerDelivery: float, costPerProduct: float, fixedPrice: float) -> None:
        self.costPerDelivery = costPerDelivery
        self.costPerProduct = costPerProduct
        self.fixedPrice = fixedPrice