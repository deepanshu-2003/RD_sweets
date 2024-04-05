from django.shortcuts import render,redirect,HttpResponse
from Home.models import Order,OrderDetail,Product,Cancelled_order
from django.contrib import messages
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
        order_data['expected']=item.expected
        order_data['cancelled']=item.cancelled
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
    return render(request,"orders.html",{'orders':my_orders})


def  order_detail(request,id):    
    order = Order.objects.filter(id=id,username=request.user.username).first()
    if order==None:
        messages.error(request,"Specified order doesn't exists.")
        return redirect('Home')
    order_detail = OrderDetail.objects.filter(order_id=order.id)
    order_context = {}
    order_context['order_id']=order.id
    order_context['items']=[]
    order_context['amount']=order.amount
    order_context['order_date']=order.order_date
    order_context['order_time']=order.order_time
    order_context['expected']=order.expected
    if(order.ready and order.out and order.dilivered):
        order_context['status']='Dilivered'
    elif(order.ready and order.out):
        order_context['status']='Out for Dilivery'
    elif(order.ready):
        order_context['status']="Ready"
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