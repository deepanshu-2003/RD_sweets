from cart.models import CartItem

def count_items(request):
    total_items_in_cart = CartItem.objects.filter(username=request.user.username).count()
    return {'total_items':total_items_in_cart}
