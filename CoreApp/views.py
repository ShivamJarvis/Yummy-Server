from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from CoreApp.models import AddressDetail, Customer, User
from django.contrib.auth import login
import math
import random
from datetime import datetime
from django.db.models import Q
from CoreApp.serializers import AddressDetailSerializer, CustomerSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
def getOTP(length):
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(length) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

class CustomerUserHandler(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request,format=None):
        username = request.data.get('username')
        
        user = User.objects.filter(Q(username=username) | Q(email=username) | Q(mobile_no=username)).first()
        
        otp = getOTP(6)
        
        if user:
            user.current_otp = otp
            user.otp_request_time = datetime.now()
            user.save()
            
            return Response({
                        "message":"OTP Send",
                        "otp":otp,
                        
                    },status=status.HTTP_200_OK)
        
        if username.isnumeric():
            new_user = User.objects.create(
                username = username,
                
                mobile_no=username,
                current_otp=otp
                
            )
            
        else:
            new_user = User.objects.create(
                username = username,
                
                email=username,
                current_otp=otp
            )
            
        new_user.set_password(User.objects.make_random_password())
            
        new_customer = Customer.objects.create(user=new_user)
        new_customer.save()
        
        new_user.save()

        return Response({
                        "message":"OTP Send",
                        "otp":otp,
                        
                    },status=status.HTTP_200_OK)

class CustomerLoginHandler(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request,format=None):
        username = request.data.get('username')
        otp = request.data.get('otp')
        
        
        
        user = User.objects.filter(Q(username=username) | Q(email=username) | Q(mobile_no=username)).first()
       
       
        if user and user.current_otp == otp and abs((user.otp_request_time.replace(tzinfo=None) - datetime.now()).total_seconds()) // 60 <= 3 :
            
            login(request,user)
            
            user.save()
            token = get_tokens_for_user(user)
            return Response({
                        "message":"User Logined",
                        "token":token,
                        
                    },status=status.HTTP_200_OK)
            
        return Response({"message":"Wrong OTP or Seems OTP Expired"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
     

class CustomerDetailsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):

        user = request.user
        customer_details = Customer.objects.filter(user=user).first()
        
        if not customer_details:
            return Response({"message":"Customer Not Found"},status=status.HTTP_404_NOT_FOUND)
        
        customer_serializer = CustomerSerializer(customer_details)

        return Response({"message":"Success","data":customer_serializer.data},status=status.HTTP_200_OK)
    
    def put(self,request,format=None):

        user = request.user
        customer_details = Customer.objects.filter(user=user).first()
        
        if not customer_details:
            
            return Response({"message":"Customer Not Found"},status=status.HTTP_404_NOT_FOUND)
        
        customer_serializer = CustomerSerializer(customer_details,data=request.data,partial=True)
        if customer_serializer.is_valid(raise_exception=True):
            customer_serializer.save()
            return Response({"message":"Success","data":customer_serializer.data},status=status.HTTP_200_OK)
        
        return Response(customer_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class AddressDetailAPI(ListAPIView):
    queryset = AddressDetail.objects.all()
    serializer_class = AddressDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
   
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )
    
class AddressCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,format=None):
        user = request.user
        data = request.data
        try:
            address_line_1 = data['address_line_1']
        except:
            address_line_1 = ""
            
        if address_line_1 == "":
            return Response({
                        "message":"No Data Found",
                        "status":"success",
                    },status=status.HTTP_404_NOT_FOUND)

        try:
            address_line_2 = data['address_line_2']
        except:
            address_line_2 = ""

        
        try:
            zip_code = data['zip_code']
        except:
            zip_code = ""

        try:
            landmark = data['landmark']
        except:
            landmark = ""

        try:
            address_type = data['address_type']
        except:
            address_type = ""
        
        if address_type == "":
            return Response({
                        "message":"Please select address type",
                        "status":"success",
                    },status=status.HTTP_404_NOT_FOUND)

        try:
            reciever_name = data['reciever_name']
        except:
            reciever_name = ""
        
        if reciever_name == "":
            return Response({
                        "message":"Reciever name not found",
                        "status":"success",
                    },status=status.HTTP_404_NOT_FOUND)

        try:
            reciever_phone_no = data['reciever_phone_no']
        except:
            reciever_phone_no = ""
            
        if reciever_name == "":
            return Response({
                        "message":"Reciever phone no. not found",
                        "status":"success",
                    },status=status.HTTP_404_NOT_FOUND)

        try:
            longitude = data['longitude']
        except:
            longitude = ""

        try:
            latitude = data['latitude']
        except:
            latitude = ""

        try:
            other_name = data['other_name']
        except:
            other_name = ""

        try:
            instructions = data['instructions']
        except:
            instructions = ""
        address = AddressDetail.objects.create(
            user = user,
            address_line_1 = address_line_1,
            address_line_2 = address_line_2,
            zip_code = zip_code,
            landmark = landmark,
            address_type = address_type,
            reciever_name = reciever_name,
            reciever_phone_no = reciever_phone_no,
            longitude = longitude,
            latitude = latitude,
            other_name = other_name,
            instructions = instructions,

            )
        
        address.save()
       
        address_data = AddressDetailSerializer(address)
        return Response({
                        "data":address_data.data,
                        "status":"success",
                    },status=status.HTTP_200_OK)
        
    

class AddressDeleteAPIView(APIView):    
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        address = AddressDetail.objects.filter(id=int(request.data.get('address_id'))).filter(user=user).first()
        
        if not address:
            return Response({"message":"No address Found","status":"fail"},status=status.HTTP_401_UNAUTHORIZED)
            
        address.delete()
        return Response({"message":"Address Deleted","status":"success"},status=status.HTTP_200_OK)
    
