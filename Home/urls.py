from django.contrib import admin
from django.urls import path
from Home import views
urlpatterns = [
    path('',views.index,name='Home'),
    path('about/',views.about,name='about'),
    path('search/',views.search_item,name='search_item'),
    path('product/<int:pno>',views.product,name="product"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('register/',views.register_user,name="register"),
]
