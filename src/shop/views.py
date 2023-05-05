from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.http import HttpResponse


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    print(products)

    template_name = "shop/product/list.html"
    context = {
        "category": category,
        "categories": categories,
        "products": products,
        "categories": categories,
    }

    return render(request, template_name, context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)

    template_name = "shop/product/detail.html"
    context = {
        "product": product,
    }
    return render(request, template_name, context)
