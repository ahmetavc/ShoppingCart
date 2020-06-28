from __future__ import annotations
import DiscountType

class Campaign:

    def __init__(self, category: Category, discount: float, minItemLimit: int, discountType: DiscountType) -> None:
        self.category = category
        self.discount = discount
        self.minItemLimit = minItemLimit
        self.discountType = discountType