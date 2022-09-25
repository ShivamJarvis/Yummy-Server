from django.contrib import admin
from RestrauntApp.models import Restraunt,RestrauntBranch,RestrauntMenu,RestrauntMenuHead,Category

# Register your models here.


admin.site.register(Category)
admin.site.register(Restraunt)
admin.site.register(RestrauntBranch)

admin.site.register(RestrauntMenu)
admin.site.register(RestrauntMenuHead)