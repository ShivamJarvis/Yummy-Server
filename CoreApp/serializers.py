from rest_framework import serializers
from CoreApp.models import User,Customer,AddressDetail




class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressDetail
        fields = "__all__"
        
   

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        
   
    

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = '__all__'
        
   
    
