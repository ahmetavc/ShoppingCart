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
               'productCount': 3,
               'currentPrice': 15.0,
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

    def addItem(self, product: Product, count: int) -> bool:
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
                    curProductDiscountAmount = self.categories[applicableCategory.title]['products'][curProduct]['currentPrice'] * (discount / 100.0)
                    curCategoryDiscountAmount += curProductDiscountAmount
                    self.categories[applicableCategory.title]['products'][curProduct]['currentPrice'] -= curProductDiscountAmount

                self.categories[applicableCategory.title]['currentPrice'] -= curCategoryDiscountAmount
                self.campaignDiscount += curCategoryDiscountAmount
                self.currentTotalAmount -= curCategoryDiscountAmount

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
        
    def getTotalAmountAfterDiscounts(self) -> float:
        pass

    def getCouponDiscounts(self) -> float:
        return self.couponDiscount
    
    def getCampaignDiscounts(self) -> float:
        return self.campaignDiscount

    def print(self) -> None:
        pass

    
