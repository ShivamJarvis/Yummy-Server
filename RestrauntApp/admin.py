from django.contrib import admin
from RestrauntApp.models import CustomDishHead, CustomisationOptions, DiscountCoupon, Order, OrderItem, Restraunt,RestrauntMenu,RestrauntMenuHead,Category,Cart,CartItems,CartCustomisedItem,RestrauntSection,Banner,Cuisine,AppliedCoupon


# Register your models here.


admin.site.register(Category)
admin.site.register(Restraunt)


admin.site.register(RestrauntMenu)
admin.site.register(RestrauntMenuHead)

admin.site.register(CustomDishHead)
admin.site.register(CustomisationOptions)

admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(CartCustomisedItem)


admin.site.register(RestrauntSection)
admin.site.register(Banner)
admin.site.register(Cuisine)
admin.site.register(DiscountCoupon)
admin.site.register(AppliedCoupon)
admin.site.register(Order)
admin.site.register(OrderItem)