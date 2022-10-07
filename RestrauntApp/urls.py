from django.urls import path
from RestrauntApp import views

urlpatterns = [
    
    path('',views.RestrauntsListAPI.as_view()),
    path('<pk>',views.RestrauntsDetailAPI.as_view()),
    path('menu-heads/',views.RestrauntMenuHeadListAPI.as_view()),
    path('cart/',views.CartAPIView.as_view()),
    path('cart/load/',views.LoadCartAPIView.as_view()),
    path('cart/add-item/',views.AddItemCartAPIView.as_view()),
    path('cart/remove-item/',views.RemoveItemCartAPIView.as_view()),
    path('cart/item/',views.CartItemDetailAPI.as_view()),
    
]