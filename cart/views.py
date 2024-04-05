from django.shortcuts import render,redirect
from cart.models import CartItem,MetaCart
from Home.models import Product
from django.contrib import messages
from decimal import Decimal
# Create your views here.

def cart_summary(request):
    cart = CartItem.objects.filter(username=request.user.username)
    charges = Decimal(0.00)
    total = Decimal(0.00)
    amount=Decimal(0.00)
    discount = Decimal(0.00)
    products=[]
    for i in cart:
        prod=Product.objects.get(id=i.product_id)
        amount=Decimal(round(Product.objects.get(id=i.product_id).price*i.quantity,2))
        products.append([prod,i.quantity,amount])
        total=total+amount
    if(amount>=0 and amount<100):
        charges=(total*25)/100
    elif(amount>=100 and amount<200):
        charges=(total*20)/100
    elif(amount>=200 and amount<500):
        charges=(total*10)/100
    else:
        charges=(total*5)/100
    grand_total = total+charges
    net_amount = Decimal(0.00)
    net_amount=grand_total-discount
    if MetaCart.objects.filter(user=request.user.username).count() >0:
        MetaCart.objects.filter(user=request.user.username).delete()
    
    conf_cart = MetaCart(user=request.user.username,items=len(products),amount=total,charges=charges,total=grand_total,discount=discount,net=net_amount)
    conf_cart.save()
    
    return render(request,"cart_summary.html",{'items':products,'amount':total,'charges':charges,'g_total':grand_total,'discount':discount,'net':net_amount})

def cart_add(request,pno):
    if request.method=="POST":
        product_id = pno
        user = request.user.username
        qty = request.POST['qty']
        if CartItem.objects.filter(username=user,product_id=product_id).count()<1:
            new = CartItem.objects.create(username=user,product_id=product_id,quantity=qty)
            new.save()
            messages.success(request,"Item is successfully added to cart")
            return redirect('Home')
        else:
            messages.warning(request,"Item is already in cart")
            return redirect('Home')
def cart_delete(request,pno):
    item = CartItem.objects.filter(product_id=pno)
    item.delete()
    return redirect('cart_summary')
