from Category import Category
from Campaign import Campaign
from Product import Product
from DiscountType import DiscountType
from Coupon import Coupon
from typing import List, Tuple

class ShoppingCart:

    def __init__(self) -> None:
        """
        example categories structure;
        categories = {
            'categoryTitle': {
               'obj': category,
               'productCount': 4,
               'currentPrice': 35.0,
               'products': {
                   'product1title': {
                       'obj': product1,
                       'count': 3,
                       'currentPrice': 10.0,
                   },
                   'product2title': {
                       'obj': product2,
                       'count': 1,
                       'currentPrice': 5.0,
                   }
               }     
            },
            'cat2': {
                ..
            }
        }
        """
        self.categories: dict = dict()
        self.currentTotalAmount: float = 0
        self.couponDiscount: float = 0
        self.campaignDiscount: float = 0
        self.numberOfUniqueProducts: int = 0
        self.isAnyDiscountApplied: bool = False
        self.deliveryCost: float = None # will be calculated when deliveryCostCalculator calculates the cost

    def addItem(self, product: Product, count: int) -> bool:
        # if any discount is applied, items cannot be changes. This will be changed in the future releases
        if self.isAnyDiscountApplied:
            False

        category = product.category
        currentProductPrice = product.price * count
        self.currentTotalAmount += currentProductPrice

        if category.title in self.categories:
            self.categories[category.title]['productCount'] += count
            self.categories[category.title]['currentPrice'] += currentProductPrice

            if product.title in self.categories[category.title]['products']:
                self.categories[category.title]['products'][product.title]['count'] += count
                self.categories[category.title]['products'][product.title]['currentPrice'] += currentProductPrice
            else:
                self.numberOfUniqueProducts += 1
                self.categories[category.title]['products'][product.title] = {
                    'obj': product,
                    'count': count,
                    'currentPrice': currentProductPrice
                }    
        else:
            self.numberOfUniqueProducts += 1
            self.categories[category.title] = {
                'obj': category,
                'productCount': count,
                'currentPrice': currentProductPrice,
                'products': {
                    product.title : {
                        'obj': product,
                        'count': count,
                        'currentPrice': currentProductPrice
                    }
                }
            }

        return True, 'Items are succesfully added to your shopping cart!'

    def applyDiscounts(self, *campaigns: Campaign) -> None:
        self.isAnyDiscountApplied = True
        rateDiscountCampaigns = []
        amountDiscountsCampaigns = []

        # in order to apply maximum discount,
        # rate discounts should be applied before amount discounts.
        for campaign in campaigns:
            if campaign.discountType == DiscountType.Amount:
                amountDiscountsCampaigns.append(campaign)
            else:
                rateDiscountCampaigns.append(campaign)

        self.applyRateDiscountCampaigns(rateDiscountCampaigns)
        self.applyAmountDiscountCampaigns(amountDiscountsCampaigns)

    def applyRateDiscountCampaigns(self, rateDiscounts: List[Campaign]) -> None:
        for campaign in rateDiscounts:
            applicableCategories, applicableProductCount = self.getCampaignApplicableCategories(campaign)
            discount = campaign.discount if campaign.discount <= 100.0 else 100.0

            # if there is not enough products in all the categories affected by this campaign, continue
            if applicableProductCount <= campaign.minProductLimit:
                continue

            for applicableCategory in applicableCategories:
                curCategoryDiscountAmount = 0
                for curProduct in self.categories[applicableCategory.title]['products']:
                    curProductCurrentPrice = self.categories[applicableCategory.title]['products'][curProduct]['currentPrice']
                    curProductDiscountAmount = curProductCurrentPrice * (discount / 100.0)
                    self.categories[applicableCategory.title]['currentPrice'] -= curProductDiscountAmount
                    self.categories[applicableCategory.title]['products'][curProduct]['currentPrice'] -= curProductDiscountAmount
                    self.campaignDiscount += curProductDiscountAmount
                    self.currentTotalAmount -= curProductDiscountAmount

    # Discount amount is discounted from every applicable category (children categories too) equally
    # Discount amount in a category affects every product according to its price ratio in the category
    def applyAmountDiscountCampaigns(self, amountDiscounts: List[Campaign]) -> None: 
        for campaign in amountDiscounts:
            applicableCategories, applicableProductCount = self.getCampaignApplicableCategories(campaign)

            # if there is not enough products in all the categories affected by this campaign, continue
            if applicableProductCount <= campaign.minProductLimit:
                continue

            for applicableCategory in applicableCategories:
                totalPriceOfCategoryBeforeDiscount = self.categories[applicableCategory.title]['currentPrice']
                discount = campaign.discount if campaign.discount <= totalPriceOfCategoryBeforeDiscount else totalPriceOfCategoryBeforeDiscount

                for curProduct in self.categories[applicableCategory.title]['products']:
                    curProductCurrentPrice = self.categories[applicableCategory.title]['products'][curProduct]['currentPrice']
                    curProductDiscountAmount = discount * (curProductCurrentPrice / totalPriceOfCategoryBeforeDiscount) 
                    self.categories[applicableCategory.title]['products'][curProduct]['currentPrice'] -= curProductDiscountAmount

                self.categories[applicableCategory.title]['currentPrice'] -= discount
                self.campaignDiscount += discount
                self.currentTotalAmount -= discount
            
    def getCampaignApplicableCategories(self, campaign: Campaign) -> Tuple[List[Category], int]:
        category = campaign.category
        applicableCategories = []
        applicableProductCount = 0

        for curCategoryTitle in self.categories:
            curCategory = self.categories[curCategoryTitle]['obj']
            parentCategory = curCategory

            # campaign category also affects its child categories
            while parentCategory != None:
                if parentCategory.title == category.title:
                    applicableCategories.append(curCategory)
                    applicableProductCount += self.categories[curCategoryTitle]['productCount']
                    break

                parentCategory = parentCategory.parent

        return applicableCategories, applicableProductCount

    def applyCoupon(self, coupon: Coupon) -> bool:
        if self.currentTotalAmount < coupon.minPurchaseLimit:
            return False

        self.isAnyDiscountApplied = True

        if coupon.discountType == DiscountType.Amount:
            discount = coupon.discount if coupon.discount <= self.currentTotalAmount else self.currentTotalAmount
        else:                        
            discount = coupon.discount if coupon.discount <= 100.0 else 100.0

        totalAmountBeforeDiscount = self.currentTotalAmount

        for category in self.categories:
            for product in self.categories[category]['products']:
                productCurrentPrice = self.categories[category]['products'][product]['currentPrice']

                if coupon.discountType == DiscountType.Amount:
                    productDiscount = discount * (productCurrentPrice / totalAmountBeforeDiscount)
                else:
                    productDiscount = productCurrentPrice * (discount / 100.0)
                
                self.categories[category]['currentPrice'] -= productDiscount
                self.categories[category]['products'][product]['currentPrice'] -= productDiscount
                self.currentTotalAmount -= productDiscount
                self.couponDiscount += productDiscount

        return True
        
    def getTotalAmountAfterDiscounts(self) -> float:
        return self.currentTotalAmount

    def getCouponDiscounts(self) -> float:
        return self.couponDiscount
    
    def getCampaignDiscounts(self) -> float:
        return self.campaignDiscount

    def getDeliveryCost(self) -> float:
        return self.deliveryCost

    def print(self) -> None:
        
        for category in self.categories:
            for product in self.categories[category]['products']:
                count = self.categories[category]['products'][product]['count']
                unitPrice = self.categories[category]['products'][product]['obj'].price
                totalPrice = self.categories[category]['products'][product]['currentPrice']
                totalDiscount = unitPrice * count - totalPrice

                print("CategoryName: {}, ProductName: {}, Quantity: {}, UnitPrice: {}, TotalPrice: {}, TotalDiscount: {}".format(
                    category, 
                    product, 
                    count,
                    unitPrice,
                    totalPrice,
                    totalDiscount
                ))

        print("TotalCost: {}, DeliveryCost: {}".format(self.currentTotalAmount, self.deliveryCost))

    
