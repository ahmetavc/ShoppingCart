from Category import Category
from ShoppingCart import ShoppingCart
from Product import Product
import unittest

class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
    
    def test_add_the_first_product_for_a_new_category(self):  
        newCategory = Category('new')
        firstProduct = Product('firstProduct', 100.0, newCategory)
        self.cart.addItem(firstProduct, 1)

        expectedCategoryProductCount = 1
        expectedCategoryCurrentPrice = 100.0
        expectedProductCount = 1
        expectedProductCurrentPrice = 100.0

        self.assertEqual(self.cart.categories['new']['productCount'], expectedCategoryProductCount) 
        self.assertEqual(self.cart.categories['new']['currentPrice'], expectedCategoryCurrentPrice)
        self.assertEqual(self.cart.categories['new']['products']['firstProduct']['count'], expectedProductCount)
        self.assertEqual(self.cart.categories['new']['products']['firstProduct']['currentPrice'], expectedProductCurrentPrice)
        self.assertEqual(self.cart.numberOfUniqueProducts, 1)
        self.assertEqual(self.cart.currentTotalAmount, 100.0)

    def test_add_a_product_to_already_existing_category(self):
        existingCategory = Category('existingCategory')
        firstProduct = Product('firstProduct', 100.0, existingCategory)
        secondProduct = Product('secondProduct', 200.0, existingCategory)
        self.cart.addItem(firstProduct, 1)
        self.cart.addItem(secondProduct, 1)

        expectedCategoryProductCount = 2
        expectedCategoryCurrentPrice = 300.0
        expectedSecondProductCount = 1
        expectedSecondProductCurrentPrice = 200.0

        self.assertEqual(self.cart.categories['existingCategory']['productCount'], expectedCategoryProductCount) 
        self.assertEqual(self.cart.categories['existingCategory']['currentPrice'], expectedCategoryCurrentPrice)
        self.assertEqual(self.cart.categories['existingCategory']['products']['secondProduct']['count'], expectedSecondProductCount)
        self.assertEqual(self.cart.categories['existingCategory']['products']['secondProduct']['currentPrice'], expectedSecondProductCurrentPrice)
        self.assertEqual(self.cart.numberOfUniqueProducts, 2)
        self.assertEqual(self.cart.currentTotalAmount, 300.0)

    def test_add_the_same_product_again(self):
        category = Category('category')
        product = Product('product', 100.0, category)
        self.cart.addItem(product, 1)
        self.cart.addItem(product, 1)

        expectedCategoryProductCount = 2
        expectedCategoryCurrentPrice = 200.0
        expectedProductCount = 2
        expectedProductCurrentPrice = 200.0

        self.assertEqual(self.cart.categories['category']['productCount'], expectedCategoryProductCount) 
        self.assertEqual(self.cart.categories['category']['currentPrice'], expectedCategoryCurrentPrice)
        self.assertEqual(self.cart.categories['category']['products']['product']['count'], expectedProductCount)
        self.assertEqual(self.cart.categories['category']['products']['product']['currentPrice'], expectedProductCurrentPrice)
        self.assertEqual(self.cart.numberOfUniqueProducts, 1)
        self.assertEqual(self.cart.currentTotalAmount, 200.0)

if __name__ == '__main__':
    unittest.main()


