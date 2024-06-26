from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class Customer(models.Model):
    profile_pic = models.ImageField(upload_to='profiles/', default = "profiles/default_profile_pic_128491.jpg")
    user=models.CharField(max_length = 50,default="admin")
    phone = models.CharField(max_length = 10,blank=True)
    address = models.CharField(max_length= 150,blank = True)
    postal_code = models.CharField(blank=True,max_length= 150)
    city = models.CharField(max_length= 150,blank=True)
    state = models.CharField(max_length= 150,blank=True)
    country = models.CharField(max_length= 150,blank=True)
    block = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user


class Product(models.Model):
    name = models.CharField(max_length = 50)
    price = models.DecimalField(default = 0,decimal_places = 2 , max_digits = 10)
    available_quantity = models.DecimalField(default = 0.00,decimal_places = 2 , max_digits = 10)
    description = models.CharField(max_length = 100 ,default = '',blank= True,null=True)
    image = models.ImageField(upload_to='products/')
    list = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    username=models.CharField(max_length=50,blank=True)
    order_date = models.DateField(default = datetime.datetime.today())
    order_time = models.TimeField(default=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time())
    payment = models.BooleanField(default=False)
    amount = models.DecimalField(default=0.00,decimal_places=2,max_digits=10)
    expected =  models.TimeField(default=(timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()) + datetime.timedelta(minutes=45)).time())
    ready = models.BooleanField(default=False)
    out = models.BooleanField(default=False)
    dilivered = models.BooleanField(default=False)
    cancelled = models.BooleanField(default = False)
    def __str__(self):
        return f"Order ID : {self.id} ; User ID : {self.username}"

class OrderDetail(models.Model):
    order_id = models.IntegerField(max_length=10)
    product_id = models.IntegerField(max_length=10)
    quantity = models.DecimalField(default=0.00,decimal_places=2,max_digits=10)
    
    
    def __str__(self):
        return f"Order ID : {str(self.order_id)} ; Product ID : {str(self.product_id)}"

class Cancelled_order(models.Model):
    order_id = models.IntegerField()
    cancelled_date = models.DateField(default=datetime.datetime.today())
    cancelled_time = models.TimeField(default = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time())
    reason = models.CharField(max_length=200,blank=True)
    
    def __str__(self) -> str:
        return "ID : "+str(self.order_id)
class Dilivered_order(models.Model):
    order_id = models.IntegerField()
    dilivery_date = models.DateField(default=datetime.datetime.today())
    dilivery_time = models.TimeField(default = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time())
    
    def __str__(self) -> str:
        return "ID : "+str(self.order_id)
class Activity(models.Model):
    user = models.CharField(max_length=60,default="admin")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    date = models.DateField(default = datetime.datetime.today())
    time = models.TimeField(default = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time())
    def __str__(self):
        return f"{self.user} -> {self.title}"