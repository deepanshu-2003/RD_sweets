from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Activity,Order,OrderDetail,Dilivered_order,Cancelled_order
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.models import User

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
