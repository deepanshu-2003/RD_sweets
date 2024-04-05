from django.urls import path
from cart import views

urlpatterns = [
    path('',views.cart_summary,name='cart_summary'),
    path('add/<int:pno>',views.cart_add,name='cart_add'),
    path('delete/<int:pno>',views.cart_delete,name='cart_del'),
  
]