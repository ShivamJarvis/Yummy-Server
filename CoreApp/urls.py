from django.urls import path
from CoreApp import views

urlpatterns = [
    path('get-cutomer-otp/',views.CustomerUserHandler.as_view()),
    path('login-cutomer-otp/',views.CustomerLoginHandler.as_view()),
    path('cutomer-details/',views.CustomerDetailsAPI.as_view()),
]