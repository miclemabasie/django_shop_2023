from django.contrib import admin
from .models import Order, OrderItem

# for administration task on data import and export
import csv
import datetime
from django.http import HttpResponse


# def export_to_csv(modeladmin, request, queryset):
#     opts = modeladmin.model._meta
#     content_disposition = f"attacthment; filename={opts.verbose_name}.csv"
#     response = HttpResponse(content_type="text/csv")
#     response["Content-Disposition"] = content_disposition
#     writer = csv.writer(response)

#     fields = [
#         field
#         for field in opts.get_fields()
#         if not field.many_to_many and not field.one_to_many
#     ]
#     # write a first row with header information
#     writer.writerow([field.verbose_name for field in fields])
#     # Write data rows
#     for obj in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(obj, field.name)
#             if isinstance(value, datetime.datetime):
#                 value = value.strftime("%d/%m/%Y")
#             data_row.append(data_row)
#         writer.writerow(data_row)
#     return response


def export_to_csv(modeladmin, request, queryset):
    # Get model metadata
    opts = queryset.model._meta

    # Set up HTTP response headers
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{opts.verbose_name}.csv"'

    # Create CSV writer object
    writer = csv.writer(response)

    # Write header row
    writer.writerow(
        [
            field.verbose_name
            for field in opts.fields
            if not field.many_to_many and not field.one_to_many
        ]
    )

    # Write data rows
    for obj in queryset:
        writer.writerow(
            [
                getattr(obj, field.name)
                if not isinstance(getattr(obj, field.name), datetime.datetime)
                else getattr(obj, field.name).strftime("%Y-%m-%d %H:%M:%S")
                for field in opts.fields
                if not field.many_to_many and not field.one_to_many
            ]
        )

    return response


export_to_csv.short_description = "Export selected objects to CSV"

export_to_csv.short_description = "Export to CSV"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "created",
        "updated",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
