from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from datetime import datetime
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username,is_email,is_phone_no):
        if not username:
            raise ValueError('Please provide mobile no. or email in username field')
        
        user = self.model(username=username)
        if is_email:
            user.email = username
        
        if is_phone_no:
            user.mobile_no = username
        user.set_password(self.make_random_password())
        user.save()
        return user
    
    def create_superuser(self,username,password=None):
        if not username:
            raise ValueError('Please provide mobile no. or email in username field')
        
        user = self.model(username=username)
        
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    mobile_no = models.CharField(max_length=13,unique=True,null=True,blank=True)
    current_otp = models.CharField(max_length=6,null=True,blank=True)
    otp_request_time = models.DateTimeField(default=datetime.now())
    email = models.EmailField(verbose_name="email address",max_length=255,unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_head_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_delivery_partner = models.BooleanField(default=False)
    is_restraunt_partner = models.BooleanField(default=False)
    is_password_secured = models.BooleanField(default=False)
    profile_photo = models.ImageField(null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    
    def __str__(self) -> str:
        return self.username
    
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer_user")
    total_orders_count = models.IntegerField(default=0)
    total_cancellation_count = models.IntegerField(default=0)
    is_cod_applicable = models.BooleanField(default=True)
    
    