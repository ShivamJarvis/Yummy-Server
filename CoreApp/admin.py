from django.contrib import admin
from CoreApp.models import Customer, User, AddressDetail
# Register your models here.


class UserDetails(admin.ModelAdmin):
    list_display = ['username','name','email','mobile_no','is_superuser','is_staff','is_restraunt_partner','is_customer','is_delivery_partner']
    list_filter = ['created_at','updated_at','is_restraunt_partner','is_customer','is_staff','is_delivery_partner']
    list_per_page = 100


admin.site.register(User,UserDetails)
admin.site.register(Customer)
admin.site.register(AddressDetail)