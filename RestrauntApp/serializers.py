from rest_framework import serializers
from RestrauntApp.models import Restraunt,RestrauntBranch,RestrauntMenu,RestrauntMenuHead


class RestrauntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restraunt
        fields = '__all__'

class RestrauntMenuSerializer(serializers.ModelSerializer):
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
        
   