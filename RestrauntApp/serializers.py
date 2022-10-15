from dataclasses import field
from rest_framework import serializers
from RestrauntApp.models import Banner, Cart, CartCustomisedItem, Cuisine, DiscountCoupon, Order, Restraunt,RestrauntMenu,RestrauntMenuHead,CustomDishHead,CustomisationOptions,CartItems, RestrauntSection


class RestrauntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restraunt
        fields = '__all__'

class CustomisationOptionserializer(serializers.ModelSerializer): 
    class Meta:
        model = CustomisationOptions
        fields = '__all__'
        

class CustomDishHeadSerializer(serializers.ModelSerializer): 
    custom_dish_head = CustomisationOptionserializer(many=True)
    class Meta:
        model = CustomDishHead
        fields = '__all__'
        
    
  
class RestrauntMenuSerializer(serializers.ModelSerializer):
    dish = CustomDishHeadSerializer( many=True)
    image = serializers.ImageField(
            max_length=None, use_url=True
        )
    class Meta:
        model = RestrauntMenu
        exclude = ['menu_head']
    

class RestrauntMenuHeadSerializer(serializers.ModelSerializer):
    menu = RestrauntMenuSerializer( many=True)
    
    class Meta:
        model = RestrauntMenuHead
        fields = '__all__'
        
class CartCustomisedItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartCustomisedItem
        fields = "__all__"
        depth=1
class CartItemSerializer(serializers.ModelSerializer):
    cart_item = CartCustomisedItemSerializer(many=True)
    class Meta:
        model = CartItems
        exclude = ['cart']
        depth=1
        
class CartSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True)
    restraunt = RestrauntSerializer()
    class Meta:
        model = Cart
        fields = '__all__'
        
class RestrauntSectionSerializer(serializers.ModelSerializer):
    restraunts = RestrauntSerializer(many=True)
    class Meta:
        model = RestrauntSection
        fields = '__all__'
        
        
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'     
        
class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = '__all__'

class CuisineDetailSerializer(serializers.ModelSerializer):
    restraunt_cuisine = RestrauntSerializer(many=True)
    class Meta:
        model = Cuisine
        fields = '__all__'
        
class DiscountSouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCoupon
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
        
