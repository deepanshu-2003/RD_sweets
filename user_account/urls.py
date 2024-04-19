from django.urls import path
from . import views


urlpatterns = [
    path('orders/',views.orders,name="orders"),
    path('order/<int:id>',views.order_detail,name="order_details"),
    path('cancel/',views.order_cancel,name="order_cancel"),
    path('profile/',views.profile,name="profile"),
]
