from django.shortcuts import render

# Create your views here.
def dilivery_home(request):
    return render(request,"dilivery.html",{})