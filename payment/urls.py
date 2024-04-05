from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.detail,name="checkout"),
    path('payment/',views.payment,name="payment"),
    path('create_checkout_session/', views.create_checkout_session, name='pay'),
    path('cancel/', views.cancel, name='cancel'),
    path('success/', views.success, name='success'),
]
