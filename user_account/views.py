from django.shortcuts import render,redirect,HttpResponse
from Home.models import Order,OrderDetail,Product,Cancelled_order,Dilivered_order
from django.contrib import messages
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
# Create your views here.
def  orders(request):
    my_orders = []
    
    orders = Order.objects.filter(username=request.user.username)
    if orders.count()==0:
        messages.warning(request,"You don't have any order yet !!! , order now... ")
        return redirect('Home')
    for item in orders:
        order_detail = OrderDetail.objects.filter(order_id=item.id)
        order_data = {}
        order_data['order_id']=item.id
        order_data['items']=[]
        order_data['amount']=item.amount
        order_data['order_date']=item.order_date
        order_data['order_time']=item.order_time
        if not item.cancelled and not item.dilivered:
            order_data['expected']=item.expected
        elif item.dilivered:
            dilivery = Dilivered_order.objects.filter(order_id=item.id).first()
            order_data['dilivered_date']=dilivery.dilivery_date
            order_data['dilivered_time']=dilivery.dilivery_time
        else:
            cancelled = Cancelled_order.objects.filter(order_id=item.id).first()
            order_data['cancelled_date']=cancelled.cancelled_date
            order_data['cancelled_time']=cancelled.cancelled_time
        # order_data['cancelled']=item.cancelled
        if(item.ready and item.out and item.dilivered):
            order_data['status']='Dilivered'
        elif(item.ready and item.out):
            order_data['status']='Out for Dilivery'
        elif(item.ready):
            order_data['status']="Ready"
        elif(item.cancelled):
            order_data['status']='Cancelled'
        else:
            order_data['status']='Confirmed'

        if(item.payment):
            order_data['payment']="Paid"
        else:
            order_data['payment']="Pending"
            
        for i in order_detail:
            prod = Product.objects.get(id=i.product_id)
            order_data['items'].append([prod.image,prod.name,i.quantity])
        my_orders.append(order_data)
    
    # print(my_orders)
    my_orders.reverse()
    return render(request,"orders.html",{'orders':my_orders})


def  order_detail(request,id):    
    order = Order.objects.filter(id=id).first()
    if order==None or (order.username != request.user.username and not request.user.is_superuser):
        messages.error(request,"Specified order doesn't exists.")
        return redirect('Home')
    order_detail = OrderDetail.objects.filter(order_id=order.id)
    order_context = {}
    order_context['order_id']=order.id
    if request.user.is_superuser:
        user = User.objects.get(username = order.username)
        order_context['user'] = [user.username,user.first_name,user.last_name]
    order_context['items']=[]
    order_context['amount']=order.amount
    order_context['order_date']=order.order_date
    order_context['order_time']=order.order_time
    if not order.cancelled and not order.dilivered:
        order_context['expected']=order.expected
    elif order.dilivered:
        dilivery = Dilivered_order.objects.filter(order_id=order.id).first()
        order_context['dilivered_date']=dilivery.dilivery_date
        order_context['dilivered_time']=dilivery.dilivery_time
        
    else:
        cancelled = Cancelled_order.objects.filter(order_id=order.id).first()
        order_context['cancelled_date']=cancelled.cancelled_date
        order_context['cancelled_time']=cancelled.cancelled_time
    if(order.ready and order.out and order.dilivered):
        order_context['status']='Dilivered'
    elif(order.ready and order.out):
        order_context['status']='Out for Dilivery'
    elif(order.ready):
        order_context['status']="Ready"
    elif(order.cancelled):
        order_context['status']='Cancelled'
    else:
        order_context['status']='Confirmed'
            

    if(order.payment):
        order_context['payment']="Paid"
    else:
        order_context['payment']="Pending"
            
    for i in order_detail:
        prod = Product.objects.get(id=i.product_id)
        order_context['items'].append([prod.image,prod.name,i.quantity])
    
    return render(request,"order_detail.html",{'order':order_context})

def order_cancel(request):
    if request.method == "POST":
        print(request.POST)
        order = Order.objects.get(id=request.POST['order_id'])
        order.cancelled=True
        order.save()
        cancel = Cancelled_order(order_id=request.POST['order_id'],reason=request.POST['reason'],cancelled_date=datetime.datetime.today(),cancelled_time=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time())
        cancel.save()
        orders = OrderDetail.objects.filter(order_id = request.POST['order_id'])
        for item in orders:
            prod = Product.objects.get(id = item.product_id)
            prod.available_quantity+=item.quantity
            prod.save()
        messages.success(request,"Your ordered cancelled successfully.. ")
        return redirect('Home')
    try:
        order = Order.objects.get(id=request.GET['order_id'])
    except Exception as e :
        messages.error(request,"Order cannot be cancelled!! ")
        return redirect('Home')
    if order.username != request.user.username or order.cancelled == True:
        messages.error(request,"Order cannot be cancelled!! ")
        return redirect('Home')
    else:
        return render(request,"order_cancel.html",{'order_id':request.GET['order_id']})