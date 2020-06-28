import DiscountType

class Coupon:

    def __init__(self, minPurchaseLimit: float, discount: float, discountType: DiscountType):
        self.minPurchaseLimit = minPurchaseLimit
        self.discount = discount
        self.discountType = discountType