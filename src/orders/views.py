# Administrative work
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order

from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.cart import Cart
from .tasks import order_created
from django.core.mail import send_mail

# Pdf generation
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


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
                    price=item["price"],
                )
            # Clear the cart
            cart.clear()
            # Launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session["order_id"] = order.id
            # redirect for payment
            return redirect(reverse("payment:process"))

            template_name = "orders/order/created.html"
            context = {"order": order}
            return render(request, template_name, context)
    context = {
        "cart": cart,
        "form": form,
    }
    template_name = "orders/order/create.html"

    return render(request, template_name, context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template_name = "admin/orders/order/detail.html"
    context = {
        "order": order,
    }

    return render(request, template_name, context)


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {"order": order}
    template_name = "orders/order/pdf.html"
    html = render_to_string(template_name, context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disosition"] = f"filename=order_{order.id}.pd"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + "css/pdf.css")]
    )
    return response
