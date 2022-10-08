from django.contrib import admin
from RestrauntApp.models import CustomDishHead, CustomisationOptions, Restraunt,RestrauntMenu,RestrauntMenuHead,Category,Cart,CartItems,CartCustomisedItem

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