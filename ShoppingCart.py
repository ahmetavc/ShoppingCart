import Category
import Product
import Campaign
import DiscountType
import Coupon

class ShoppingCart:

    def __init__(self) -> None:
        """
        example categories structure;
        categories = {
            'cat1': {
               'obj': cat1,
               'productCount': 3,
               'currentPrice': 15.0,
               'products': {
                   'prod11': {
                       'obj': prod11,
                       'count': 3,
                       'currentPrice': 10.0,
                   },
                   'prod12': {
                       'obj': prod12,
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
            False, 'You cannot add new items after discounts are applied!'

        category = product.category
        currentProductPrice = product.price * count

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

    def getTotalAmountAfterDiscounts(self) -> float:
        pass

    def getCouponDiscounts(self) -> float:
        return self.couponDiscount
    
    def getCampaignDiscounts(self) -> float:
        return self.campaignDiscount

    def print(self) -> None:
        pass

    
