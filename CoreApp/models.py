from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,User
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
        user.set_password = User.objects.make_random_password()
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,password):
        if not username:
            raise ValueError('Please provide mobile no. or email in username field')
        
        user = self.model(username=username)
        
        user.set_password = password
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    mobile_no = models.CharField(max_length=13,unique=True,null=True,blank=True)
    email = models.EmailField(verbose_name="email address",max_length=255,unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
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