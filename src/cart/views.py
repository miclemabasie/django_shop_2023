from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"])

    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    template_name = "cart/detail.html"
    context = {
        "cart": cart,
    }
    return render(request, template_name, context)


# Test function for data submissions


@csrf_exempt
def testing(request):
    if request.method == "POST":
        print("This is a post request")
        print(request.POST)
        data = {
            "name": request.POST.get("username"),
            "password": request.POST.get("password"),
        }

        return JsonResponse(data, safe=False)
    return HttpResponse("This is some testing page")
