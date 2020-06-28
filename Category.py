from __future__ import annotations

class Category:

    def __init__(self, title: str, parent: Category = None) -> None:
        self.title = title
        self.parent = parent