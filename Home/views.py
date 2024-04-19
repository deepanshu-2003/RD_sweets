from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Activity,Order,OrderDetail,Dilivered_order,Cancelled_order,Customer
from payment.models import Payment
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your views here.
def index(request):
    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(list = True)
    return render(request,'index.html',{'products':products,})

def about(request):
    return render(request,'about.html',{})


def product(request,pno):
    product=Product.objects.get(id=pno)
    return render(request,"product.html",{'product':product})



def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["passwd"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            cust = Customer.objects.filter(user = username).first()
            if cust == None:
                cust = Customer(user = username)
                cust.save()
            if cust.block:
                messages.error(request, "Your user id is banned by administrator")
                return redirect('login')
            login(request,user)
            messages.success(request,"You have successfully been logged in . ")
            return redirect('Home')
        else:
            messages.error(request, "Your credentials are invalid , Try again...")
            return redirect('login')
    else:
        return render(request,'login.html',{})
def logout_user(request):
    logout(request)
    messages.success(request,"You have been successfully logged out. ")
    return redirect('Home')
def register_user(request):
    if request.method =="POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]        
        email = request.POST["email"]
        username = request.POST["username"]   
        passwd1 = request.POST["password1"]        
        passwd2 = request.POST["password2"]
        if not passwd1 == passwd2:
            messages.warning(request,"Confirmation password is different from previous one")
            return redirect('register')
        
        # creating new user here ...
        # return HttpResponse("<h1>Hello welcome</h1>")
        try:
            user = User.objects.create_user(username,email,passwd1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request,"You have successfully been registered")
            return redirect('login')
        except Exception as e:
            if str(e).startswith("UNIQUE constraint failed"):
                messages.error(request,'Username already exists try some other')
                return redirect('register')
            else:
                messages.error(request,'Something went wrong')
                return redirect('register')
                
    else:
        return render(request,'register.html',{})


def search_item(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query)
    return render(request,"index.html",{'products':products})

#  -----------------operations for only super user-------------------------
def unlist_prod(request,pno):
    try:
        if request.user.is_superuser:
            prod = Product.objects.get(id=pno)
            prod.list = False
            prod.save()
            messages.success(request,"product unlisted successfully")
            return redirect('Home')
        else:
            messages.error(request,"Internal server error occured.")
            return redirect('Home')
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')


def list_prod(request,pno):
    try:
        if request.user.is_superuser:
            prod = Product.objects.get(id=pno)
            prod.list = True
            prod.save()
            messages.success(request,"product listed successfully")
            return redirect('Home')
        else:
            messages.error(request,"Internal server error occured.")
            return redirect('Home')
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
        
        

def edit_prod(request,pno):
    if not request.user.is_superuser:
        messages.error(request,"Invalid operation")
        return redirect('Home') 
    if request.method == "POST":
        try:
            product = Product.objects.get(id=pno)
            product.name=request.POST['name']
            product.description = request.POST['description']
            product.price = request.POST['price']
            product.available_quantity = request.POST['available_quantity']
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            messages.success(request,"Product is saved with changes successfully.")
            return redirect('Home')
        except:
            messages.error(request,"Internal server error occured.")
            return redirect('Home')
    try:
        product = Product.objects.get(id=pno)
        return render(request,'super_user/edit_product.html',{'product':product})
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')


def add_prod(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                Product(name=request.POST['name'],price=request.POST['price'],available_quantity=request.POST['available_quantity'],description=request.POST['description'],image=request.FILES['image']).save()
                messages.success(request,"Product added successfully.")
                return redirect('Home')
            except:
                messages.error(request,"Internal server error occured.")
                return redirect('Home')
        return render(request,'super_user/add_product.html',{})
    else:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')

def activity(request):
    activities = Activity.objects.all()
    activities.reverse()
    return render(request,'super_user/activity.html',{'activities':activities})

def close_activity(request,id):
    try:
        Activity.objects.get(id = id).delete()
        return redirect('activity')
    except:
        messages.error(request,"Internal servere error occured.")
        return redirect('Activity')


def all_orders(request):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    all_orders = []
    
    orders = Order.objects.all()
    if orders.count()==0:
        messages.warning(request,"Don't have any order yet !!! , order now... ")
        return redirect('Home')
    for item in orders:
        order_detail = OrderDetail.objects.filter(order_id=item.id)
        order_data = {}
        user = User.objects.get(username = item.username)
        order_data['user'] =[user.username,user.first_name,user.last_name]
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
        all_orders.append(order_data)
    
    # print(my_orders)
    all_orders.reverse()
    return render(request,"orders.html",{'orders':all_orders})

def order_ready(request,id):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    try:
        order = Order.objects.get(id = id)
        order.ready = True
        order.save()
        messages.success(request,"Order marked to ready.")
        return redirect('orders')
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
def order_out(request,id):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    try:
        order = Order.objects.get(id = id)
        order.out = True
        order.save()
        messages.success(request,"Order marked to Out.")
        return redirect('orders')
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    
def order_diliver(request,id):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    try:
        order = Order.objects.get(id = id)
        order.dilivered = True
        order.save()
        dilivered = Dilivered_order(order_id = id,dilivery_date = datetime.datetime.today(),dilivery_time = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time())
        dilivered.save()
        messages.success(request,"Order marked to dilivered.")
        return redirect('orders')
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    
def payment_cash(request,id):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    try:
        order = Order.objects.get(id = id)
        order.payment = True
        order.save()
        payment = Payment(order_id = id,user=order.username,payment_mode = "Cash",payment_date = datetime.datetime.today(),payment_time = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time(),amount=order.amount)
        payment.save()
        messages.success(request,"Payment made successfully.")
        return redirect('orders')
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    
def pending_orders(request):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    pending_orders = []
    
    orders = Order.objects.filter(dilivered = False,cancelled = False)
    if orders.count()==0:
        messages.warning(request,"Don't have any pending order... ")
        return redirect('Home')
    for item in orders:
        order_detail = OrderDetail.objects.filter(order_id=item.id)
        order_data = {}
        user = User.objects.get(username = item.username)
        order_data['user'] =[user.username,user.first_name,user.last_name]
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
        pending_orders.append(order_data)
    
    # print(my_orders)
    pending_orders.reverse()
    return render(request,"orders.html",{'orders':pending_orders})

def all_customer(request):
    customers = []
    users = User.objects.all()
    for user in users:
        customer = {}
        cust = Customer.objects.filter(user = user.username).first()
        if cust == None :
            cust = Customer(user = user.username,phone = "")
            cust.save()
        customer['profile_pic']=cust.profile_pic
        customer['username']=user.username
        customer['block']=cust.block
        customer['first_name']=user.first_name
        customer['last_name']=user.last_name
        if cust is not None:
            customer['address'] = f"{cust.address}, {cust.city}, {cust.state}, {cust.country}"
            customer['postal_code']=cust.postal_code
            customer['phone']=cust.phone
            customer['email']=user.email
        customers.append(customer)
    print(customers)
    # return HttpResponse(customers)
    return render(request,'super_user/customers.html',{'customers':customers})


def edit_customer(request,user):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    try:
        if request.method == 'POST':
            customer = Customer.objects.get(user = user)
            usr = User.objects.get(username = user)
            usr.first_name = request.POST['first_name']
            usr.last_name = request.POST['last_name']
            usr.email = request.POST['email']
            usr.save()
            if 'profile_pic' in request.FILES:
                customer.profile_pic = request.FILES['profile_pic']
            customer.address = request.POST['address']
            customer.city = request.POST['city']
            customer.state = request.POST['state']
            customer.country = request.POST['country']
            customer.phone = request.POST['phone']
            customer.postal_code = request.POST['postal_code']
            customer.save()
            messages.success(request,"customer details edited successfully.")
            return redirect('all_customer')
        cust = Customer.objects.get(user=user)
        usr = User.objects.get(username = user)
        customer = {
            'profile_pic':cust.profile_pic,
            'username':cust.user,
            'block':cust.block,
            'first_name':usr.first_name,
            'last_name':usr.last_name,
            'email':usr.email,
            'phone':cust.phone,
            'address':cust.address,
            'state':cust.state,
            'city':cust.city,
            'country':cust.country,
            'postal_code':cust.postal_code,    
        }
        return render(request,'super_user/edit_customer.html',{'customer':customer})
    except Exception as e:
        messages.error(request,f"Internal server error occured. {e}")
        return redirect('Home')
        

def block_customer(request,user):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    try:
        cust = Customer.objects.get(user=user)
        cust.block = True
        cust.save()
        messages.success(request,"User blocked successfully")
        return redirect('all_customer')
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
        
def unblock_customer(request,user):
    if not request.user.is_superuser:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
    try:
        cust = Customer.objects.get(user=user)
        cust.block = False
        cust.save()
        messages.success(request,"Unblocked user successfully")
        return redirect('all_customer')
    except:
        messages.error(request,"Internal server error occured.")
        return redirect('Home')
        
    