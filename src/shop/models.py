from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=200, verbose_name=_("Category Name"), db_index=True
    )
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", kwargs={"slug": self.slug})


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=200, db_index=True, verbose_name=_("Product Name")
    )
    slug = models.SlugField(max_length=200, db_index=True, verbose_name=_("Slug"))
    image = models.ImageField(
        upload_to="products/%Y/%m/%d", blank=True, verbose_name=_("Image")
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Price")
    )
    available = models.BooleanField(default=True, verbose_name=_("Availability"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Date Updated"))

    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"id": self.id, "slug": self.slug})
