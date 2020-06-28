from __future__ import annotations
from Category import Category

class Product:

    def __init__(self, title: str, price: float, category: Category) -> None:
        self.title = title
        self.price = price
        self.category = category


    