from __future__ import annotations
import DiscountType

class Campaign:

    def __init__(self, category: Category, discount: float, minProductLimit: int, discountType: DiscountType) -> None:
        self.category = category
        self.discount = discount
        self.minProductLimit = minProductLimit
        self.discountType = discountType