from django.contrib import admin
from django.urls import path
from dilivery import views
urlpatterns = [
    path('',views.dilivery_home,name='dilivery'),
    
]
