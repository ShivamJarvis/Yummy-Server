from email.policy import default
from turtle import back
from django.db import models

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


class RestrauntBranch(models.Model):
    restraunt = models.ForeignKey(Restraunt,on_delete=models.CASCADE,null=True,blank=True,related_name="restraunt_branches")
    outlet_name = models.CharField(max_length=100,null=True,blank=True)
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
    
    def __str__(self) -> str:
        return self.outlet_name
    
    
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
    is_veg = models.BooleanField(default=False)
    open_time = models.TimeField(null=True,blank=True)
    close_time = models.TimeField(null=True,blank=True)
    rating = models.FloatField(default=4.2)
    total_sell = models.IntegerField(default=0)
    
    
    def __str__(self) -> str:
        return f"{self.item_name}"
    