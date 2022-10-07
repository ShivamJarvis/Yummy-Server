from email.policy import default
from turtle import back
from django.db import models

from CoreApp.models import User

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name
    

class Restraunt(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="restraunt_category")
    card_image = models.ImageField(null=True,blank=True)
    head_image = models.ImageField(null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    latitude = models.CharField(max_length=100,null=True,blank=True)
    longitude = models.CharField(max_length=100,null=True,blank=True)
    fssai_no = models.CharField(max_length=100,null=True,blank=True)
    fssai_certificate = models.FileField(null=True,blank=True)
    rating = models.FloatField(default=4.2)
    owner_name = models.CharField(max_length=100,null=True,blank=True)
    address_line_1 = models.CharField(max_length=100,null=True,blank=True)
    address_line_2 = models.CharField(max_length=100,null=True,blank=True)
    address_line_3 = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    zip_code = models.CharField(max_length=100,null=True,blank=True)
    joined_at = models.DateField(auto_now_add=True)
    description = models.TextField(null=True,blank=True)
    closing_timing = models.TimeField(null=True,blank=True)
    opening_timing = models.TimeField(null=True,blank=True)
    maximum_delivery_radius = models.IntegerField(default=3)
    
    def __str__(self) -> str:
        return self.name



    
    
class RestrauntMenuHead(models.Model):
    restraunt = models.ForeignKey(Restraunt,on_delete=models.CASCADE,null=True,blank=True,related_name="restraunt_menu")
    name = models.CharField(max_length=100,null=True,blank=True)
    open_time = models.TimeField(null=True,blank=True)
    close_time = models.TimeField(null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.restraunt.name})"
    
    
class RestrauntMenu(models.Model):
    menu_head = models.ManyToManyField(RestrauntMenuHead,related_query_name="menu",related_name="menu")
    item_name = models.CharField(max_length=100,null=True,blank=True)
    item_price = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    is_bestseller = models.BooleanField(default=False)
    is_healthy = models.BooleanField(default=False)
    is_customisable = models.BooleanField(default=False)
    is_veg = models.BooleanField(default=False)
    open_time = models.TimeField(null=True,blank=True)
    close_time = models.TimeField(null=True,blank=True)
    rating = models.FloatField(default=4.2)
    total_sell = models.IntegerField(default=0)
    
    
    def __str__(self) -> str:
        return f"{self.item_name} {self.id}"
    
    
class CustomDishHead(models.Model):
    menu_dish = models.ManyToManyField(RestrauntMenu,related_query_name="dish",related_name="dish")
    name = models.CharField(max_length=100,null=True,blank=True)
    max_selection = models.IntegerField(default=1)
    min_selection = models.IntegerField(default=1)
    is_required = models.BooleanField(default=False)
    is_additional_amount_calculated = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return f"{self.name} ({self.id})"
    
    
class CustomisationOptions(models.Model):
    custom_dish = models.ForeignKey(CustomDishHead,on_delete=models.CASCADE,null=True,blank=True,related_name="custom_dish_head")
    name = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(default=0)
    
    
    def __str__(self) -> str:
        return f"{self.custom_dish.name} ({self.name})"
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="cart_user")
    cart_total = models.FloatField(default=0)
    restraunt = models.ForeignKey(Restraunt,on_delete=models.CASCADE,null=True,blank=True,related_name="restraunt_cart")
    

class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True,related_name="cart")
    qty = models.IntegerField(default=1)
    item = models.ForeignKey(RestrauntMenu,on_delete=models.CASCADE,null=True,blank=True,related_name="menu_item")
    item_total = models.FloatField(default=0)
    
    
class CartItemsCustomisationHead(models.Model):
    cart_item = models.ForeignKey(CartItems,on_delete=models.CASCADE,null=True,blank=True,related_name="cart_item")
    customisation_option = models.ForeignKey(CustomisationOptions,on_delete=models.CASCADE,null=True,blank=True,related_name="cart_customisation_option")
    price = models.FloatField(default=0)
    

    