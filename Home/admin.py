from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header="RD sweets"
admin.site.site_title="RD sweets"
admin.site.index_title="RD sweets"


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Cancelled_order)
