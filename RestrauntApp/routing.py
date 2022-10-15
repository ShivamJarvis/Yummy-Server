from django.urls import path

from RestrauntApp import consumers

websocket_urlpatterns = [
    path('ws/restraunt/<id>/', consumers.NewOrderConsumer.as_asgi()),
    path('ws/order/<order_id>/', consumers.OrderConsumer.as_asgi()),
]