from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Payment(models.Model):
    order_id = models.IntegerField(max_length=10)
    user = models.CharField(max_length=50)
    payment_mode = models.CharField(max_length=50)
    payment_date = models.DateField(default = datetime.datetime.today())
    payment_time = models.TimeField(default=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time())
    amount = models.DecimalField(default=0.00,decimal_places=2,max_digits=10)
    def __str__(self) -> str:
        return "Order ID : "+str(self.order_id) +" ; User ID : "+self.user