from cart.models import CartProduct, Cart
from clinic.settings import SHIPPING_COST, SHIPPING_FREE_AFTER
from django.shortcuts import render, redirect
from django.utils.timezone import now
from moneyed import Money

from panel.models import Product
from panel.views import PanelView


class ShoppingCartView(PanelView):
    def get(self, request):
        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            cart = Cart(customer=request.user, lastUpdated=now)
            cart.save()

        items = CartProduct.objects.filter(cart=cart)
        total_price = 0
        for item in items:
            item.totalPrice = item.quantity * item.product.price
            total_price += item.totalPrice

        if total_price >= SHIPPING_FREE_AFTER:
            shipping_cost = None
            cost_after_shipping = total_price

        else:
            shipping_cost = SHIPPING_COST
            cost_after_shipping = shipping_cost + total_price

        context = {'items': items, 'total_price': total_price, "shipping_cost": shipping_cost,
                   "cost_after_shipping": cost_after_shipping}
        return render(request, 'cart/shopping_cart.html', context)

    def post(self, request):
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            product = None

        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            cart = Cart(customer=request.user, lastUpdated=now)
            cart.save()

        cart_products = CartProduct.objects.filter(cart=cart.id)
        does_exist = False
        for cart_product in cart_products:
            if cart_product.product == product:
                cart_product.quantity += int(quantity)
                cart_product.save()
                does_exist = True
                break
        if not does_exist:
            CartProduct(product=product, cart=cart, quantity=quantity).save()
        return redirect('cart:cart')


