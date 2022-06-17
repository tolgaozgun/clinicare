from cart.models import CartProduct, Cart
from django.shortcuts import render
from django.utils.timezone import now
from panel.views import PanelView


class ShoppingCartView(PanelView):
    def get(self, request):
        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            cart = Cart(customer=request.user, lastUpdated=now)
            cart.save()

        items = CartProduct.objects.filter(cart=cart)
        totalPrice = 0
        for item in items:
            item.totalPrice = item.quantity * item.product.price
            totalPrice += item.totalPrice
        context = {'items': items, 'totalPrice': totalPrice}
        return render(request, 'cart/shopping_cart.html', context)

