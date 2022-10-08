from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from RestrauntApp.models import Cart, CartCustomisedItem, CartItems, CustomDishHead, CustomisationOptions, Restraunt, RestrauntMenu, RestrauntMenuHead
from RestrauntApp.serializers import CartItemSerializer, CartSerializer, CustomDishHeadSerializer, RestrauntSerializer,RestrauntMenuHeadSerializer
# Create your views here.

class RestrauntsListAPI(ListAPIView):
    queryset = Restraunt.objects.all()
    serializer_class = RestrauntSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'rating': ['gte', 'lte']
    }

class RestrauntsDetailAPI(RetrieveAPIView):
    queryset = Restraunt.objects.all()
    serializer_class = RestrauntSerializer
    permission_classes = [permissions.AllowAny]
    



class RestrauntMenuHeadListAPI(ListAPIView):
    queryset = RestrauntMenuHead.objects.all()
    serializer_class = RestrauntMenuHeadSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restraunt']
  
class CustomDishHeadListAPI(ListAPIView):
    queryset = CustomDishHead.objects.all()
    serializer_class = CustomDishHeadSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['menu_dish']
  


class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    
    def delete(self,request,format=None):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return Response({
                        "message":"No Cart Found",
                        "status":"error",
                        
                    },status=status.HTTP_404_NOT_FOUND)
        
        cart.delete()
        return Response({"message":"Cart Deleted",
                         "status":"success", 
                    },status=status.HTTP_200_OK)
        
        


class LoadCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        
        
        user = request.user
    
        cart = Cart.objects.filter(user=user).first()
        
        if not cart:
            return Response({"data":{},"status":"success"},status=status.HTTP_200_OK)
        
        cart_data = CartSerializer(cart)
        
        return  Response({"data":cart_data.data,"status":"success"},status=status.HTTP_200_OK)
        

class AddItemCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        
        restrauntId = request.data.get('restrauntId')
        itemId = request.data.get('itemId')
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            restraunt = Restraunt.objects.filter(id=int(restrauntId)).first()
            cart = Cart.objects.create(user=user,restraunt=restraunt)
            cart.save() 
            
        restraunt = Restraunt.objects.filter(id=int(restrauntId)).first()
        cart = Cart.objects.filter(user=user).filter(restraunt=restraunt).first()
        item = RestrauntMenu.objects.filter(id=int(itemId)).first()
        cart_item = CartItems.objects.filter(cart=cart).filter(item=item).first()
        
        if not cart_item:
            cart_item = CartItems.objects.create(cart=cart,item=item,item_total=item.item_price)
            cart_item.save()
        else:
            cart_item.qty = int(cart_item.qty) + 1
            cart_item.item_total = float(int(cart_item.qty) * float(item.item_price))
            cart_item.save()
        
        cart_total = 0
        for i in cart.cart.all():
            cart_total += float(i.item_total)
            
        cart.cart_total = cart_total
        
        cart.save()
        
        return Response({"message":"Item Added to Cart","status":"success"},status=status.HTTP_200_OK)

class RemoveItemCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        
        restrauntId = request.data.get('restrauntId')
        itemId = request.data.get('itemId')
        user = request.user
    
        restraunt = Restraunt.objects.filter(id=int(restrauntId)).first()
        cart = Cart.objects.filter(user=user).filter(restraunt=restraunt).first()
   

        if not cart:
            return Response({
                        "message":"No Cart Found",
                        "status":"error",
                        
                    },status=status.HTTP_404_NOT_FOUND)
            
      
        item = RestrauntMenu.objects.filter(id=int(itemId)).first()
        cart_item = CartItems.objects.filter(cart=cart).filter(item=item).first()
        
        if cart_item.qty > 1:
            cart_item.qty = int(cart_item.qty) - 1
            cart_item.item_total = float(int(cart_item.qty) * float(item.item_price))
            cart_item.save()
        else:
            cart_item.delete()
     
            
        cart_total = 0
        for i in cart.cart.all():
            cart_total += float(i.item_total)
            
        cart.cart_total = cart_total
        
        cart.save()
        
        return Response({"message":"Item Removed to Cart","status":"success"},status=status.HTTP_200_OK)
    
    
class CartItemDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        restrauntId = request.data.get('restrauntId')
        itemId = request.data.get('itemId')
        user = request.user
    
        restraunt = Restraunt.objects.filter(id=int(restrauntId)).first()
        cart = Cart.objects.filter(user=user).filter(restraunt=restraunt).first()
        if not cart:
            return Response({
                        "message":"No Cart Found",
                        "status":"error",
                        
                    },status=status.HTTP_200_OK)
            
        item = RestrauntMenu.objects.filter(id=int(itemId)).first()
        if not item:
            return Response({
                        "message":"No Item Found",
                        "status":"error",
                        
                    },status=status.HTTP_200_OK)
            
        cart_item = CartItems.objects.filter(cart=cart).filter(item=item).all()
        if not cart_item:
            return Response({
                        "message":"No Cart Item Found",
                        "status":"error",
                        
                    },status=status.HTTP_200_OK)
        
        if not item.is_customisable:
            cart_item = cart_item.first()
        else:
            qty = 0
            for i in cart_item:
                qty += int(i.qty)
            
            cart_item = cart_item.first()
            cart_item.qty = qty
   
        cart_item = CartItemSerializer(cart_item)
      
        
        
        return Response({"message":"Success","data":cart_item.data},status=status.HTTP_200_OK)
    
    
class AddCustomisedItemCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        
        restrauntId = request.data.get('restrauntId')
        itemId = request.data.get('itemId')
        customisation_options = request.data.get('customisedOptions')
        is_repeated = request.data.get('isRepeated')
        user = request.user
        
        restraunt = Restraunt.objects.filter(id=int(restrauntId)).first()
    
        cart = Cart.objects.filter(user=user).filter(restraunt=restraunt).first()
        
   

        if not cart:
            cart = Cart.objects.create(user=user,restraunt=restraunt)
            cart.save() 
            
        
        item = RestrauntMenu.objects.filter(id=int(itemId)).first()
        cart_item = CartItems.objects.filter(cart=cart).filter(item=item).last()
        
        if not is_repeated or not cart_item:
           
            cart_item = CartItems.objects.create(cart=cart,item=item,item_total=item.item_price)
            cart_item.save()

            for option in customisation_options:
                for custom_item in option['custom_dish_head']:
                    try:
                        
                        if custom_item['select'] and custom_item['select'] == True:
                            customisation_option = CustomisationOptions.objects.filter(id=custom_item['id']).first()
                            new_cart_custom_item = CartCustomisedItem.objects.create(cart_item=cart_item,customisation_option=customisation_option)
                            new_cart_custom_item.save()
                    except:
                        pass
                        
        elif is_repeated and cart_item:
            
            cart_item.qty = int(cart_item.qty) + 1
            cart_item.item_total = float(int(cart_item.qty) * float(item.item_price))
            cart_item.save()
            
        
        for i in cart.cart.all():
            item_price_total = 0
            for j in i.cart_item.all():
                item_price_total += float(float(j.customisation_option.price) * int(i.qty))
            i.item_total = float(item_price_total) + float(i.item_total)
            i.save()
                
       
        cart_total = 0
        for i in cart.cart.all():
            cart_total += float(i.item_total)
            
        cart.cart_total = cart_total
        
        cart.save()
        
        return Response({"message":"Customised Item Added to Cart","status":"success"},status=status.HTTP_200_OK)
    
class RemoveCustomisedItemCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        
        restrauntId = request.data.get('restrauntId')
        itemId = request.data.get('itemId')
        user = request.user
    
        restraunt = Restraunt.objects.filter(id=int(restrauntId)).first()
        cart = Cart.objects.filter(user=user).filter(restraunt=restraunt).first()
   

        if not cart:
            return Response({
                        "message":"No Cart Found",
                        "status":"error",
                        
                    },status=status.HTTP_404_NOT_FOUND)
            
      
        item = RestrauntMenu.objects.filter(id=int(itemId)).first()
        cart_item = CartItems.objects.filter(cart=cart).filter(item=item).all()
        
        if len(cart_item) > 1:
            return Response({
                        "message":"Remove of multi item not possible",
                        "status":"success",
                        
                    },status=status.HTTP_200_OK)
            
        cart_item = cart_item.first()
                
        if cart_item.qty > 1:
            cart_item.qty = int(cart_item.qty) - 1
            item_total = float(int(cart_item.qty) * float(item.item_price))
            
            item_price_total = 0
            for j in i.cart_item.all():
                item_price_total += float(float(j.customisation_option.price) * int(i.qty))
            
            cart_item.item_total = float(item_price_total) + float(item_total)
            cart_item.save()
        else:
            cart_item.delete()
     
            
        cart_total = 0
        for i in cart.cart.all():
            cart_total += float(i.item_total)
            
        cart.cart_total = cart_total
        
        cart.save()
        
        return Response({"message":"Item Removed to Cart","status":"success"},status=status.HTTP_200_OK)
    
    