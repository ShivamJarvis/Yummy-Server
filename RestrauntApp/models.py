from email.policy import default
import json
from django.db import models

from CoreApp.models import DeliveryPartner, User
import random
import string
from asgiref.sync import async_to_sync
from channels.consumer import get_channel_layer
from CoreApp.serializers import DeliveryPartnerSerializer

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name
    
class Cuisine(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    
RESTRAUNT_SERVES = (
    ('Veg','Veg'),
    ('Non-Veg','Non-Veg'),
    ('Both','Both'),
)

class Restraunt(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="restraunt_category")
    cuisine = models.ManyToManyField(Cuisine,blank=True,related_name="restraunt_cuisine")
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
    cuisine_description = models.TextField(null=True,blank=True)
    cost_of_two = models.IntegerField(default=200)
    is_exclusive = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    food_type = models.CharField(max_length=40,choices=RESTRAUNT_SERVES,default="Veg")
    
    def __str__(self) -> str:
        return f"{self.id}. {self.name}"


    
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
    preparation_time = models.IntegerField(default=0)
    
    
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
    
    
class CartCustomisedItem(models.Model):
    cart_item = models.ForeignKey(CartItems,on_delete=models.CASCADE,null=True,blank=True,related_name="cart_item")
    customisation_option = models.ForeignKey(CustomisationOptions,on_delete=models.CASCADE,null=True,blank=True,related_name="cart_customisation_option")
    
class RestrauntSection(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    restraunts = models.ManyToManyField(Restraunt,blank=True,related_name="section_restraunt")
    
    def __str__(self) -> str:
        return f'{self.name}'
    
class Banner(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    imageUrl = models.ImageField(null=True,blank=True)
    restraunt = models.ManyToManyField(Restraunt,blank=True,related_name="special_restraunt")
    
    
class DiscountCoupon(models.Model):
    code = models.CharField(max_length = 15,null=True,blank=True)
    discount_percentage = models.IntegerField(default = 0)
    description = models.TextField(null=True,blank=True)
    minimum_cart_amount = models.IntegerField(default=0)
    discount_amount_limit = models.IntegerField(default=0)
    limit_per_user = models.IntegerField(default=1)
    offer_by = models.ForeignKey(Restraunt,on_delete=models.CASCADE,null=True,blank=True,related_name="coupon_offer_by")
    
class AppliedCoupon(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="coupon_used_by")
    coupon = models.ForeignKey(DiscountCoupon,on_delete=models.CASCADE,related_name="coupon")
    

def generateOrderId():
    generated_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20))
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    
    
ORDER_STATUS = (
    ('Order Recieved','Order Recieved'),
    ('Order Confirmed','Order Confirmed'),
    ('Preparing Order','Preparing Order'),
    ('Delivery Partner at Restraunt','Delivery Partner at Restraunt'),
    ('Order Picked Up','Order Picked Up'),
    ('Delivered','Delivered'),
)
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="order_customer")
    restraunt = models.ForeignKey(Restraunt,on_delete=models.CASCADE,null=True,blank=True,related_name="restraunt_order")
    delivery_partner = models.ForeignKey(DeliveryPartner,on_delete=models.CASCADE,null=True,blank=True,related_name="delivery_partner")
    order_id = models.CharField(max_length=30,default=generateOrderId)
    order_net_amount = models.FloatField(default=0)
    order_tax_amount = models.FloatField(default=0)
    order_tip_amount = models.FloatField(default=0)
    order_delivery_amount = models.FloatField(default=0)
    order_discount_amount = models.FloatField(default=0)
    restraunt_latitude = models.FloatField(default=0)
    restraunt_longitude = models.FloatField(default=0)
    dp_latitude = models.FloatField(default=0)
    dp_longitude = models.FloatField(default=0)
    customer_latitude = models.FloatField(default=0)
    customer_longitude = models.FloatField(default=0)
    is_cod = models.BooleanField(default=False)
    item_count = models.IntegerField(default=0)
    delivery_distance = models.FloatField(default=0)
    net_delivery_time = models.FloatField(default=0)
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS,default="Order Recieved")
    customer_address = models.TextField(null=True,blank=True)
    customer_address_type = models.CharField(max_length=50,null=True,blank=True)
    order_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs ):
        
        channel_layer = get_channel_layer()
        data = {}
        data['order_id'] = self.order_id
        data['status'] = self.order_status
        
        
        try:
            if self.delivery_partner:    
                delivery_partner_data = DeliveryPartnerSerializer(self.delivery_partner)
                delivery_partner_data = delivery_partner_data.data
            else:
                delivery_partner_data = {}
        except:
            delivery_partner_data = {}
        
        data['delivery_partner'] = delivery_partner_data
        data['dp_latitude'] = self.dp_latitude
        data['dp_longitude'] = self.dp_longitude
    
        async_to_sync(channel_layer.group_send)(
            'id_%s' % self.order_id ,{
                'type':'order_status',
                'value':json.dumps(data)
            }
        )
            
            
        
        return super().save()
    
    def __str__(self) -> str:
        return self.order_id

class OrderItem(models.Model):
    item = models.ForeignKey(RestrauntMenu,on_delete=models.SET_NULL,null=True,related_name="order_item")
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,related_name="order")
    item_price = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    additional_items = models.TextField(null=True,blank=True)
    def __str__(self) -> str:
        return self.order.order_id
    
class CustomerSearches(models.Model):
    restraunt = models.ForeignKey(Restraunt,on_delete=models.CASCADE,related_name="recent_search_restraunt")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="recent_search_restraunt")
    created_at = models.DateField(auto_now_add=True)
    
    
class CustomerFavouritesRestraunt(models.Model):
    restraunt = models.ForeignKey(Restraunt,on_delete=models.CASCADE,related_name="favourite_restraunt")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_favourite_restraunt")
    created_at = models.DateField(auto_now_add=True)
    