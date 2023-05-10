from django.shortcuts import render
from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.cart import Cart
from .tasks import order_created
from django.core.mail import send_mail


def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                )
            # Clear the cart
            cart.clear()
            # Launch asynchronous task
            order_created.delay(order.id)

            template_name = "orders/order/created.html"
            context = {"order": order}
            return render(request, template_name, context)
    context = {
        "cart": cart,
        "form": form,
    }
    template_name = "orders/order/create.html"

    return render(request, template_name, context)
