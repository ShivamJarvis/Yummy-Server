from rest_framework import serializers
from RestrauntApp.models import Restraunt,RestrauntBranch,RestrauntMenu,RestrauntMenuHead,CustomDishHead,CustomisationOptions


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
        
   