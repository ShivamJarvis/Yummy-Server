from django.urls import path
from RestrauntApp import views

urlpatterns = [
    
    path('',views.RestrauntsListAPI.as_view()),
    path('sections/',views.RestrauntSectionListAPI.as_view()),
    path('banner/',views.BannerListAPI.as_view()),
    path('cuisine/',views.CuisineListAPI.as_view()),
    path('cuisine-detail/',views.CuisineDetailListAPI.as_view()),
    path('<pk>',views.RestrauntsDetailAPI.as_view()),
    path('menu-heads/',views.RestrauntMenuHeadListAPI.as_view()),
    path('custom-dish-head/',views.CustomDishHeadListAPI.as_view()),
    path('cart/',views.CartAPIView.as_view()),
    path('discount-coupon/',views.DiscountCouponAPI.as_view()),
    path('cart/load/',views.LoadCartAPIView.as_view()),
    path('cart/add-item/',views.AddItemCartAPIView.as_view()),
    path('cart/remove-item/',views.RemoveItemCartAPIView.as_view()),
    path('cart/remove-customised-item/',views.RemoveCustomisedItemCartAPIView.as_view()),
    path('cart/item/',views.CartItemDetailAPI.as_view()),
    path('cart/add-customised-item/',views.AddCustomisedItemCartAPIView.as_view()),
    path('cart/add-customised-item-cart/',views.AddCustomisedItemCartFromCartAPIView.as_view()),
    path('cart/remove-customised-item-cart/',views.RemoveCustomisedItemCartFromCartAPIView.as_view()),
    
    path('order/',views.OrderAPI.as_view()),
    path('order-detail/',views.OrderDetailListAPI.as_view()),
    
]