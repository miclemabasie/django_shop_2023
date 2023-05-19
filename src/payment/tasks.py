from celery import task
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is successfully created
    """
    order = Order.objects.get(id=order_id)

    # create invoice email
    subject = f"MIC Shop - EE Invoice No. {order.id}"
    message = "Please, find the attached invoice for yoru recent purchase"
    email = EmailMessage(
        subject,
        message,
        "admin@micshop.com",
        [order.email],
    )

    # generate PDF
    html = render_to_string("orders/order/pdf.html", {"order": order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + "css/pdf.css")]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach pdf file
    email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")

    # send email
    email.send()
