from Category import Category
from Campaign import Campaign
from Coupon import Coupon
from ShoppingCart import ShoppingCart
from Product import Product
from DiscountType import DiscountType
import unittest

class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.food = Category('food')
        self.home = Category('home')
        self.apple = Product('apple', 100.0, self.food)
        self.almond = Product('almond', 50.0, self.food)
        self.chair = Product('chair', 100.0, self.home)

        self.cart = ShoppingCart()
        self.cart.addItem(self.apple, 3)
        self.cart.addItem(self.almond, 1)
        self.cart.addItem(self.chair, 2)

        self.campaign1 = Campaign(self.food, 25.0, 1, DiscountType.Rate)
        self.campaign2 = Campaign(self.home, 50.0, 3, DiscountType.Rate)
        self.campaign3 = Campaign(self.food, 12, 1, DiscountType.Amount)
        self.campaign4 = Campaign(self.home, 10, 3, DiscountType.Amount)

        self.coupon1 = Coupon(100.0, 10.0, DiscountType.Rate)
        self.coupon2 = Coupon(1000.0, 10.0, DiscountType.Rate)
        self.coupon3 = Coupon(100.0, 100.0, DiscountType.Amount)
        self.coupon4 = Coupon(1000.0, 100.0, DiscountType.Amount)
    
    def test_should_add_the_first_product_into_a_new_category(self):  
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

    def test_should_add_a_product_into_already_existing_category(self):
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

    def test_should_add_the_same_product_again(self):
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

    def test_should_apply_rate_campaign_to_category_with_enough_products(self):
        totalPriceBeforeDiscounts = self.cart.currentTotalAmount
        curCategoryCurrentPrice = self.cart.categories['food']['currentPrice']
        curAppleProductCurrentPrice = self.cart.categories['food']['products']['apple']['currentPrice']
        curAlmondProductCurrentPrice = self.cart.categories['food']['products']['almond']['currentPrice']

        expectedCategoryDiscount = curCategoryCurrentPrice * (self.campaign1.discount / 100.0)
        expectedCategoryCurrentPrice = curCategoryCurrentPrice - expectedCategoryDiscount

        expectedAppleProductDiscount = curAppleProductCurrentPrice * (self.campaign1.discount / 100.0)
        expectedAppleProductCurrentPrice = curAppleProductCurrentPrice - expectedAppleProductDiscount

        expectedAlmondProductDiscount = curAlmondProductCurrentPrice * (self.campaign1.discount / 100.0)
        expectedAlmondProductCurrentPrice = curAlmondProductCurrentPrice - expectedAlmondProductDiscount
    
        self.cart.applyDiscounts(self.campaign1)

        self.assertEqual(self.cart.categories['food']['currentPrice'], expectedCategoryCurrentPrice) 
        self.assertEqual(self.cart.categories['food']['products']['apple']['currentPrice'], expectedAppleProductCurrentPrice)
        self.assertEqual(self.cart.categories['food']['products']['almond']['currentPrice'], expectedAlmondProductCurrentPrice)
        self.assertEqual(self.cart.campaignDiscount, expectedCategoryDiscount)
        self.assertEqual(self.cart.currentTotalAmount, totalPriceBeforeDiscounts - expectedCategoryDiscount)

    def test_should_not_apply_rate_campaign_to_category_without_enough_products(self):
        expectedCategoryCurrentPrice = self.cart.categories['home']['currentPrice']
        expectedChairProductCurrentPrice = self.cart.categories['home']['products']['chair']['currentPrice']
    
        self.cart.applyDiscounts(self.campaign2)

        self.assertEqual(self.cart.categories['home']['currentPrice'], expectedCategoryCurrentPrice) 
        self.assertEqual(self.cart.categories['home']['products']['chair']['currentPrice'], expectedChairProductCurrentPrice)

    def test_should_apply_a_campaign_to_child_categories(self):
        vegetable = Category('vegetable', self.food)
        tomato = Product('tomato', 100.0, vegetable)
        self.cart.addItem(tomato, 1)

        curCategoryCurrentPrice = self.cart.categories['vegetable']['currentPrice']
        curTomatoProductCurrentPrice = self.cart.categories['vegetable']['products']['tomato']['currentPrice']

        expectedCategoryDiscount = curCategoryCurrentPrice * (self.campaign1.discount / 100.0)
        expectedCategoryCurrentPrice = curCategoryCurrentPrice - expectedCategoryDiscount

        expectedTomatoProductDiscount = curTomatoProductCurrentPrice * (self.campaign1.discount / 100.0)
        expectedTomatoProductCurrentPrice = curTomatoProductCurrentPrice - expectedTomatoProductDiscount

        self.cart.applyDiscounts(self.campaign1)

        self.assertEqual(self.cart.categories['vegetable']['currentPrice'], expectedCategoryCurrentPrice) 
        self.assertEqual(self.cart.categories['vegetable']['products']['tomato']['currentPrice'], expectedTomatoProductCurrentPrice)

    def test_should_apply_amount_campaign_to_category_with_enough_products(self):
        totalPriceBeforeDiscounts = self.cart.currentTotalAmount
        curCategoryCurrentPrice = self.cart.categories['food']['currentPrice']
        curAppleProductCurrentPrice = self.cart.categories['food']['products']['apple']['currentPrice']
        curAlmondProductCurrentPrice = self.cart.categories['food']['products']['almond']['currentPrice']

        expectedCategoryCurrentPrice = curCategoryCurrentPrice - self.campaign3.discount

        expectedAppleProductDiscount = self.campaign3.discount * (curAppleProductCurrentPrice / curCategoryCurrentPrice)
        expectedAppleProductCurrentPrice = curAppleProductCurrentPrice - expectedAppleProductDiscount

        expectedAlmondProductDiscount = self.campaign3.discount * (curAlmondProductCurrentPrice / curCategoryCurrentPrice)
        expectedAlmondProductCurrentPrice = curAlmondProductCurrentPrice - expectedAlmondProductDiscount
    
        self.cart.applyDiscounts(self.campaign3)

        self.assertEqual(self.cart.categories['food']['currentPrice'], expectedCategoryCurrentPrice) 
        self.assertEqual(self.cart.categories['food']['products']['apple']['currentPrice'], expectedAppleProductCurrentPrice)
        self.assertEqual(self.cart.categories['food']['products']['almond']['currentPrice'], expectedAlmondProductCurrentPrice)
        self.assertEqual(self.cart.campaignDiscount, self.campaign3.discount)
        self.assertEqual(self.cart.currentTotalAmount, totalPriceBeforeDiscounts - self.campaign3.discount)

    def test_should_not_apply_amount_campaign_to_category_without_enough_products(self):
        expectedCategoryCurrentPrice = self.cart.categories['home']['currentPrice']
        expectedChairProductCurrentPrice = self.cart.categories['home']['products']['chair']['currentPrice']
    
        self.cart.applyDiscounts(self.campaign4)

        self.assertEqual(self.cart.categories['home']['currentPrice'], expectedCategoryCurrentPrice) 
        self.assertEqual(self.cart.categories['home']['products']['chair']['currentPrice'], expectedChairProductCurrentPrice)

    def test_should_apply_rate_and_amount_campaigns_together(self):
        totalPriceBeforeDiscounts = self.cart.currentTotalAmount
        curCategoryCurrentPrice = self.cart.categories['food']['currentPrice']
        curAppleProductCurrentPrice = self.cart.categories['food']['products']['apple']['currentPrice']
        curAlmondProductCurrentPrice = self.cart.categories['food']['products']['almond']['currentPrice']

        # first rate campaigns should be applied
        expectedCategoryRateDiscount = curCategoryCurrentPrice * (self.campaign1.discount / 100.0)
        expectedCategoryCurrentPriceAfterRateDiscount = curCategoryCurrentPrice - expectedCategoryRateDiscount

        expectedAppleProductRateDiscount = curAppleProductCurrentPrice * (self.campaign1.discount / 100.0)
        expectedAppleProductCurrentPriceAfterRateDiscount = curAppleProductCurrentPrice - expectedAppleProductRateDiscount

        expectedAlmondProductRateDiscount = curAlmondProductCurrentPrice * (self.campaign1.discount / 100.0)
        expectedAlmondProductCurrentPriceAfterRateDiscount = curAlmondProductCurrentPrice - expectedAlmondProductRateDiscount

        # then amount campaigns should be applied
        expectedCategoryCurrentPriceAfterAmountDiscount = expectedCategoryCurrentPriceAfterRateDiscount - self.campaign3.discount

        expectedAppleProductAmountDiscount = self.campaign3.discount * (expectedAppleProductCurrentPriceAfterRateDiscount / expectedCategoryCurrentPriceAfterRateDiscount)
        expectedAppleProductCurrentPriceAfterAmountDiscount = expectedAppleProductCurrentPriceAfterRateDiscount - expectedAppleProductAmountDiscount

        expectedAlmondProductAmountDiscount = self.campaign3.discount * (expectedAlmondProductCurrentPriceAfterRateDiscount / expectedCategoryCurrentPriceAfterRateDiscount)
        expectedAlmondProductCurrentPriceAfterAmountDiscount = expectedAlmondProductCurrentPriceAfterRateDiscount - expectedAlmondProductAmountDiscount

        self.cart.applyDiscounts(self.campaign1, self.campaign3)

        self.assertEqual(self.cart.categories['food']['currentPrice'], expectedCategoryCurrentPriceAfterAmountDiscount) 
        self.assertEqual(self.cart.categories['food']['products']['apple']['currentPrice'], expectedAppleProductCurrentPriceAfterAmountDiscount)
        self.assertEqual(self.cart.categories['food']['products']['almond']['currentPrice'], expectedAlmondProductCurrentPriceAfterAmountDiscount)
        self.assertEqual(self.cart.campaignDiscount, expectedCategoryRateDiscount + self.campaign3.discount)
        self.assertEqual(self.cart.currentTotalAmount, totalPriceBeforeDiscounts - (expectedCategoryRateDiscount + self.campaign3.discount))

    def test_should_apply_rate_coupon_with_enough_amount_on_the_cart(self):
        totalPriceBeforeDiscounts = self.cart.currentTotalAmount
        curCategoryCurrentPrice = self.cart.categories['food']['currentPrice']
        curAppleProductCurrentPrice = self.cart.categories['food']['products']['apple']['currentPrice']
        curAlmondProductCurrentPrice = self.cart.categories['food']['products']['almond']['currentPrice']

        expectedCategoryDiscount = curCategoryCurrentPrice * (self.coupon1.discount / 100.0)
        expectedCategoryCurrentPrice = curCategoryCurrentPrice - expectedCategoryDiscount

        expectedAppleProductDiscount = curAppleProductCurrentPrice * (self.coupon1.discount / 100.0)
        expectedAppleProductCurrentPrice = curAppleProductCurrentPrice - expectedAppleProductDiscount

        expectedAlmondProductDiscount = curAlmondProductCurrentPrice * (self.coupon1.discount / 100.0)
        expectedAlmondProductCurrentPrice = curAlmondProductCurrentPrice - expectedAlmondProductDiscount

        expectedTotalCouponDiscount = totalPriceBeforeDiscounts * (self.coupon1.discount / 100.0)
        expectedTotalPrice = totalPriceBeforeDiscounts - expectedTotalCouponDiscount
    
        self.cart.applyCoupon(self.coupon1)

        self.assertEqual(self.cart.categories['food']['currentPrice'], expectedCategoryCurrentPrice) 
        self.assertEqual(self.cart.categories['food']['products']['apple']['currentPrice'], expectedAppleProductCurrentPrice)
        self.assertEqual(self.cart.categories['food']['products']['almond']['currentPrice'], expectedAlmondProductCurrentPrice)
        self.assertEqual(self.cart.couponDiscount, expectedTotalCouponDiscount)
        self.assertEqual(self.cart.currentTotalAmount, expectedTotalPrice)

    def test_should_not_apply_rate_coupon_without_enough_amount_on_the_cart(self): 
        totalPriceBeforeDiscounts = self.cart.currentTotalAmount   

        self.cart.applyCoupon(self.coupon2)

        self.assertEqual(self.cart.couponDiscount, 0.0)
        self.assertEqual(self.cart.currentTotalAmount, totalPriceBeforeDiscounts)

    def test_should_apply_amount_coupon_with_enough_amount_on_the_cart(self):
        totalPriceBeforeDiscounts = self.cart.currentTotalAmount
        curCategoryCurrentPrice = self.cart.categories['food']['currentPrice']
        curAppleProductCurrentPrice = self.cart.categories['food']['products']['apple']['currentPrice']
        curAlmondProductCurrentPrice = self.cart.categories['food']['products']['almond']['currentPrice']

        expectedCategoryDiscount = self.coupon3.discount * (curCategoryCurrentPrice / totalPriceBeforeDiscounts)
        expectedCategoryCurrentPrice = curCategoryCurrentPrice - expectedCategoryDiscount

        expectedAppleProductDiscount = self.coupon3.discount * (curAppleProductCurrentPrice / totalPriceBeforeDiscounts)
        expectedAppleProductCurrentPrice = curAppleProductCurrentPrice - expectedAppleProductDiscount

        expectedAlmondProductDiscount = self.coupon3.discount * (curAlmondProductCurrentPrice / totalPriceBeforeDiscounts)
        expectedAlmondProductCurrentPrice = curAlmondProductCurrentPrice - expectedAlmondProductDiscount
    
        self.cart.applyCoupon(self.coupon3)

        self.assertEqual(self.cart.categories['food']['currentPrice'], expectedCategoryCurrentPrice) 
        self.assertEqual(self.cart.categories['food']['products']['apple']['currentPrice'], expectedAppleProductCurrentPrice)
        self.assertEqual(self.cart.categories['food']['products']['almond']['currentPrice'], expectedAlmondProductCurrentPrice)
        self.assertEqual(self.cart.couponDiscount, self.coupon3.discount)
        self.assertEqual(self.cart.currentTotalAmount, totalPriceBeforeDiscounts - self.coupon3.discount)

    def test_should_not_apply_amount_coupon_without_enough_amount_on_the_cart(self): 
        totalPriceBeforeDiscounts = self.cart.currentTotalAmount   

        self.cart.applyCoupon(self.coupon4)

        self.assertEqual(self.cart.couponDiscount, 0.0)
        self.assertEqual(self.cart.currentTotalAmount, totalPriceBeforeDiscounts)

if __name__ == '__main__':
    unittest.main()


