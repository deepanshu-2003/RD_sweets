from django.shortcuts import render,redirect,HttpResponse
from .models import Product
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    products = Product.objects.all()
    # if request.user.is_superuser:
    #     return render(request,'super_user/index.html',{'products':products,})
    return render(request,'index.html',{'products':products,})

def about(request):
    return render(request,'about.html',{})


def product(request,pno):
    product=Product.objects.get(id=pno)
    return render(request,"product.html",{'product':product})

#  -----------------operations for only super user-------------------------
def del_prod(request,pno):
    try:
        if request.user.is_superuser:
            Product.objects.get(id=pno).delete()
            messages.success(request,"product deleted successfully")
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