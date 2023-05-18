import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    print("Initializing")
    if request.method == "POST":
        # retrieve the nonce
        nonce = request.POST.get("payment_method_nonce", None)
        # create and submit transaction
        result = gateway.transaction.sale(
            {
                "amount": f"{total_cost:.2f}",
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )

        if result.is_success:
            print("Results was sucess")
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect("payment:done")
        else:
            return redirect("payment:cancelled")
    else:
        # Generate token
        client_token = gateway.client_token.generate()
        template_name = "payment/process.html"
        context = {
            "client_token": client_token,
        }
        return render(request, template_name, context)


def payment_done(request):
    return render(request, "payment/done.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")