from django.urls import path
from Home import views


app_name = "home"


urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.handle_login,name="login"),
    path('restraunt-register/',views.restraunt_register,name="restraunt_register"),
]