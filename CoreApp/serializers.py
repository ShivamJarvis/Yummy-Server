from rest_framework import serializers
from CoreApp.models import User,Customer




class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username','email','mobile_no','name']
        
   
    

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = '__all__'
        
   
    
