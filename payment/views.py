from django.shortcuts import render, redirect
from django.utils import timezone
import stripe
import datetime
from django.contrib import messages
from django.conf import settings
from Home.models import Customer
from cart.models import MetaCart,CartItem
from Home.models import Order,OrderDetail,Product
from .models import Payment as Pay
stripe.api_key = settings.STRIPE_SECRET_KEY



def create_checkout_session(request):
    cart = MetaCart.objects.filter(user=request.user.username).first()
    cust = Customer.objects.filter(user= request.user.username).first()
    product = stripe.Product.create(
        name=request.user.first_name+" "+request.user.last_name,  # Replace this with your product name
        description='Total Items : '+str(cart.items)  # Replace this with your product description
    )
    
    price = stripe.Price.create(
    product=product.id,
    unit_amount=int(cart.net*100),  # Replace this with the amount in the smallest currency unit (e.g., 1000 for ₹10.00)
    currency='inr',    # Specify currency as INR
    )
    try:
        customer=stripe.Customer.create(
            name=request.user.username,
            address={
                "line1": str(cust.address),
                "postal_code": str(cust.postal_code),
                "city": str(cust.city),
                "state": "CA",
                "country": "US",
                },
            )
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            customer=customer,
            mode='payment',
            success_url=request.build_absolute_uri('/checkout/success/'),
            cancel_url=request.build_absolute_uri('/checkout/cancel/'),
        )
        # Store the checkout session ID in the user's session
        request.session['checkout_session_id'] = checkout_session.id  # Store the session ID
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})

    return redirect(checkout_session.url, code=303)



# ---------------WORKING-------------------
def is_payment_successful(session_id):
    try:
        # Retrieve the checkout session from Stripe
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        print(checkout_session)
        # Check if the payment was successful
        if checkout_session.payment_status == 'paid':
            # Payment was successful
            return True
        else:
            # Payment was not successful
            return False
    except stripe.error.InvalidRequestError as e:
        # Handle invalid session ID or other errors
        print("ERROR: " + str(e))
        return False
    


def success(request):
    session_id = request.session.get('checkout_session_id')  # Retrieve the session ID from the session
    print(session_id)
    order = Order()
    cart = CartItem.objects.filter(username=request.user.username)
    meta = MetaCart.objects.filter(user=request.user.username).first()
    if request.method == "POST":
        mode = request.POST.get('payment_option')
        if mode == "Online":
            return redirect('pay')
        else:
            
            order.username=request.user.username
            order.order_date=datetime.datetime.today()
            order.order_time=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time()
            order.payment=False
            order.amount= meta.net
            order.expected = (timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()) + datetime.timedelta(minutes=45)).time()
            order.save()
            items = []
            for i in cart:
                order_detail = OrderDetail()
                order_detail.order_id = order.id
                order_detail.product_id =  i.product_id
                order_detail.quantity = i.quantity
                order_detail.save()
                prod = Product.objects.get(id=i.product_id)
                prod.available_quantity = prod.available_quantity - i.quantity
                items.append([prod.image,prod.name,i.quantity])
                prod.save()
                i.delete()
            MetaCart.objects.filter(user=order.username).delete()
            return render(request, "success.html", {'order':order,'items':items,'mode':'Cash on Dilivery'})
    else:
        if is_payment_successful(session_id):  # Pass session_id to the function
            order.username=request.user.username
            order.order_date=datetime.datetime.today()
            order.order_time=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time()
            order.payment=True
            order.amount= meta.net
            order.expected = (timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()) + datetime.timedelta(minutes=45)).time()
            order.save()
            items=[]
            for i in cart:
                order_detail = OrderDetail()
                order_detail.order_id = order.id
                order_detail.product_id =  i.product_id
                order_detail.quantity = i.quantity
                order_detail.save()
                prod = Product.objects.get(id=i.product_id)
                items.append([prod.image,prod.name,i.quantity])
                i.delete()
            MetaCart.objects.filter(user=order.username).delete()
            pay = Pay(order_id=order.id,user=order.username,payment_mode="Online",payment_date=datetime.datetime.today(),amount=meta.net,payment_time=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()).time())
            pay.save()
            return render(request, "success.html", {'order':order,'items':items,'mode':'Online Payment'})
        else:
            messages.error(request,"Error occured while having payment")
            return redirect('Home')




def cancel(request):
    return render(request, 'cancel.html')
def payment(request):
    if request.method =="POST":
        user = request.user.username
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        postal_code=request.POST['postal_code']
        phone = request.POST['phone']
        Customer.objects.filter(user=user).delete()
        cust = Customer(user=user,address=address,city=city,state=state,country=country,postal_code=postal_code,phone=phone)
        cust.save()
    return render(request,"payment.html",{})

def detail(request):
    if CartItem.objects.filter(username=request.user.username).count() ==  0:
        messages.warning(request,"You Dont have any Item in Cart to checkout ")
        return redirect('Home')
    else:
        cart = CartItem.objects.filter(username = request.user.username)
        for item in cart:
            prod = Product.objects.get(id = item.product_id)
            if item.quantity>prod.available_quantity:
                messages.error(request,f"{prod.name} dont have requested quantity available.")
                return redirect('Home')
        customer = Customer.objects.filter(user=request.user.username).first()
        return render(request,"details.html",{'customer':customer})
