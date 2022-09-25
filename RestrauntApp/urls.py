from django.urls import path
from RestrauntApp import views

urlpatterns = [
    
    path('',views.RestrauntsListAPI.as_view()),
    path('<pk>',views.RestrauntsDetailAPI.as_view()),
    path('menu-heads/',views.RestrauntMenuHeadListAPI.as_view()),
    
]