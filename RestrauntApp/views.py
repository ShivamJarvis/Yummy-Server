from audioop import add
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from RestrauntApp.models import AppliedCoupon, Banner, Cart, CartCustomisedItem, CartItems, Cuisine, CustomDishHead, CustomerFavouritesRestraunt, CustomerSearches, CustomisationOptions, DiscountCoupon, Order, OrderItem, Restraunt, RestrauntMenu, RestrauntMenuHead, RestrauntSection
from RestrauntApp.serializers import BannerSerializer, CartItemSerializer, CartSerializer, CuisineDetailSerializer, CuisineSerializer, CustomDishHeadSerializer, CustomerFavouritesRestrauntSerializer, CustomerSearchesSerializer, DiscountSouponSerializer, OrderItemSerializer, OrderSerializer, RestrauntSectionSerializer, RestrauntSerializer,RestrauntMenuHeadSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from CoreApp.models import AddressDetail
# Create your views here.

class RestrauntsListAPI(ListAPIView):
    queryset = Restraunt.objects.all()
    serializer_class = RestrauntSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'rating': ['gte', 'lte']
    }
    def get_queryset(self):
        return Restraunt.objects.exclude(is_approved=False)   

class RestrauntsSearchListAPI(ListAPIView):
    queryset = Restraunt.objects.all()
    serializer_class = RestrauntSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'restraunt_menu__name','restraunt_menu__menu__item_name']

class RestrauntsDetailAPI(RetrieveAPIView):
    queryset = Restraunt.objects.all()
    serializer_class = RestrauntSerializer
    permission_classes = [permissions.AllowAny]
    

class RestrauntSectionListAPI(ListAPIView):
    queryset = RestrauntSection.objects.all()
    serializer_class = RestrauntSectionSerializer
    permission_classes = [permissions.AllowAny]
    

class BannerListAPI(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]
    
class CuisineListAPI(ListAPIView):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['id']
class CuisineDetailListAPI(ListAPIView):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineDetailSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['id']



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
    
    def get(self,request,format=None):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return Response({
                        "data":{},
                        "status":"success",
                        
                    },status=status.HTTP_200_OK)
        cart_data = CartSerializer(cart)
        return Response({
                        "data":cart_data.data,
                        "status":"success",
                    },status=status.HTTP_200_OK)
    
    
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
    
    
class AddCustomisedItemCartFromCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        
        
        cartItemId = request.data.get('cartItemId')
        customisation_options = request.data.get('customisedOptions')
        is_repeated = request.data.get('isRepeated')
       
        
        cart_item = CartItems.objects.filter(id=int(cartItemId)).first()
        
        if not is_repeated:
           
            cart_item = CartItems.objects.create(cart=cart_item.cart,item=cart_item.item,item_total=cart_item.item.item_price)
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
            cart_item.item_total = float(int(cart_item.qty) * float(cart_item.item.item_price))
            cart_item.save()
            
        
       
        item_price_total = 0
        for j in cart_item.cart_item.all():
            item_price_total += float(float(j.customisation_option.price) * int(cart_item.qty))
        cart_item.item_total = float(item_price_total) + float(cart_item.item_total)
        cart_item.save()
            
        all_cart_items = CartItems.objects.filter(cart=cart_item.cart).all()
       
        cart_total = 0
        for i in all_cart_items:
            cart_total += float(i.item_total)
            
        cart_item.cart.cart_total = cart_total
        
        cart_item.cart.save()
        
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
            for j in cart_item.cart_item.all():
                item_price_total += float(float(j.customisation_option.price) * int(cart_item.qty))
            
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
    

class RemoveCustomisedItemCartFromCartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
        
        
        cartItemId = request.data.get('cartItemId')
        user = request.user
        
        cartItemId = request.data.get('cartItemId')
        cart_item = CartItems.objects.filter(id=int(cartItemId)).first()
        
        cart = cart_item.cart
        
        all_cart_items = CartItems.objects.filter(cart=cart).all()
   
                
        if cart_item.qty > 1:
            cart_item.qty = int(cart_item.qty) - 1
            item_total = float(int(cart_item.qty) * float(cart_item.item.item_price))
            
            item_price_total = 0
            for j in cart_item.cart_item.all():
                item_price_total += float(float(j.customisation_option.price) * int(cart_item.qty))
            
            cart_item.item_total = float(item_price_total) + float(item_total)
            cart_item.save()
        else:
            cart_item.delete()
     
            
        cart_total = 0
        for i in all_cart_items:
            cart_total += float(i.item_total)
            
        cart.cart_total = cart_total
        
        cart.save()
        
        return Response({"message":"Item Removed to Cart","status":"success"},status=status.HTTP_200_OK)
    
    
class DiscountCouponAPI(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        applied_coupon = AppliedCoupon.objects.filter(user=user).all()
        user_cart = Cart.objects.filter(user=user).first()
        discount_coupon = DiscountCoupon.objects.all()
        
        valid_coupon = []
        for i in discount_coupon:
            use_coupon_count = len(applied_coupon.filter(coupon=i).all())
            if i.limit_per_user > use_coupon_count and (i.offer_by == None or i.offer_by == user_cart.restraunt):
                coupon_data = DiscountSouponSerializer(i)
                valid_coupon.append(coupon_data.data)

        
        return Response({"data":valid_coupon,"status":"success"},status=status.HTTP_200_OK)
                
            
        
    
class OrderAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        restraunt = Restraunt.objects.filter(id=int(request.data.get('restraunt_id'))).first()
        order_net_amount = request.data.get('order_net_amount')
        order_tax_amount = request.data.get('order_tax_amount')
        order_tip_amount = request.data.get('order_tip_amount')
        order_delivery_amount = request.data.get('order_delivery_amount')
        order_discount_amount = request.data.get('order_discount_amount')
        restraunt_latitude = request.data.get('restraunt_latitude')
        restraunt_longitude = request.data.get('restraunt_longitude')
        customer_latitude = request.data.get('customer_latitude')
        customer_longitude = request.data.get('customer_longitude')
        is_cod = request.data.get('is_cod')
        item_count = request.data.get('item_count')
        delivery_distance = request.data.get('delivery_distance')
        customer_address = AddressDetail.objects.filter(id=int(request.data.get('customer_address'))).first()  
        
        cart = Cart.objects.filter(user=user).filter(restraunt=restraunt).first()
        
        try:
            selectedCoupon = request.data.get('selectedCoupon')
            if selectedCoupon:
                discount_coupon = DiscountCoupon.objects.filter(id=selectedCoupon).first()
                applied_coupon = AppliedCoupon.objects.create(user=user,coupon=discount_coupon)
                applied_coupon.save()
        except:
            pass
        
        
        new_order = Order.objects.create(
            user=user,
            restraunt=restraunt,
            order_net_amount=order_net_amount,
            order_tax_amount=order_tax_amount,
            order_tip_amount=order_tip_amount,
            order_delivery_amount=order_delivery_amount,
            order_discount_amount=order_discount_amount,
            restraunt_latitude=restraunt_latitude,
            restraunt_longitude=restraunt_longitude,
            customer_latitude=customer_latitude,
            customer_longitude=customer_longitude,
            is_cod=is_cod,
            item_count=item_count,
            delivery_distance=delivery_distance,
            customer_address = f'{customer_address.address_line_1}, {customer_address.address_line_2}, {customer_address.landmark}, Zip Code - {customer_address.zip_code}',
            customer_address_type = customer_address.address_type
        )
        
        new_order.save()
        
        for i in cart.cart.all():
            item = i.item
            additional_items = ""
            for additional in i.cart_item.all():
                additional_items += f"{additional.customisation_option.name}, "
                
            new_order_item = OrderItem.objects.create(
                order=new_order,
                item=item,
                item_price=item.item_price,
                additional_items=additional_items,
                qty = i.qty
            )
            new_order_item.save()
            
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(f'id_{restraunt.id}', {
        'type': 'new_order',
        'new_order_id': new_order.order_id
        })
        
        cart.delete()
        
        return Response({"order_id":new_order.order_id,"message":"Order Place Successfully","status":"success"},status=status.HTTP_200_OK)
                
            
class OrderDetailListAPI(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['order_id']
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )

class CustomerSearchesListAPI(ListAPIView):
    queryset = CustomerSearches.objects.all()
    serializer_class = CustomerSearchesSerializer
    permission_classes = [permissions.IsAuthenticated]
  
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )


class CustomerSearchesAPI(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        user = request.user
        restraunt = Restraunt.objects.filter(id=int(request.data.get('restraunt_id'))).first()
        
        no_of_old_searches = len(CustomerSearches.objects.filter(user=user).all())
        already_restraunt_in_search = CustomerSearches.objects.filter(user=user).filter(restraunt=restraunt).first()
        if no_of_old_searches >= 10:
            old_search = CustomerSearches.objects.filter(user=user).last()
            old_search.delete()
        
        if already_restraunt_in_search:
            already_restraunt_in_search.delete()
      
        
        new_search = CustomerSearches.objects.create(
            user=user,
            restraunt=restraunt,
         
        )
        
        new_search.save()
        
        
        return Response({"message":"Recent search created","status":"success"},status=status.HTTP_200_OK)
                
class CustomerFavouritesRestrauntListAPI(ListAPIView):
    queryset = CustomerFavouritesRestraunt.objects.all()
    serializer_class = CustomerFavouritesRestrauntSerializer
    permission_classes = [permissions.IsAuthenticated]
  
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )
            


