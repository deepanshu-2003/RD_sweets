from django.contrib import admin
from django.urls import path
from Home import views
urlpatterns = [
    path('',views.index,name='Home'),
    path('about/',views.about,name='about'),
    path('search/',views.search_item,name='search_item'),
    path('product/<int:pno>',views.product,name="product"),
    path('list/<int:pno>',views.list_prod,name="list_prod"),
    path('unlist/<int:pno>',views.unlist_prod,name="unlist_prod"),
    path('edit/<int:pno>',views.edit_prod,name="edit_prod"),
    path('add-product/',views.add_prod,name="add_prod"),
    path('orders/',views.all_orders,name="all_orders"),
    path('order_ready/<int:id>',views.order_ready,name="order_ready"),
    path('order_out/<int:id>',views.order_out,name="order_out"),
    path('order_diliver/<int:id>',views.order_diliver,name="order_diliver"),
    path('payment_cash/<int:id>',views.payment_cash,name="payment_cash"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('register/',views.register_user,name="register"),
    path('activity/',views.activity,name="activity"),
    path('close/<int:id>',views.close_activity,name="close_activity"),
]
