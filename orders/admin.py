import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin-order-detail', args=[obj.id])))


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def export_to_csv(modeladmin, request, queryset):
        # queryset это объекты из модели джанго 
        # ModelName.objects.all() - возвращает queryset 
        # Так же любой запрос в базу, возвращает queryset
        #   1. ModelName.objects.filter(is_active=True)
        #   2. ModelName.objects.first()
        #   3. ModelName.objects.get(pk=1)
        
        opts = modeladmin.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;' \
            'filename={}.csv'.format(opts.verbose_name)
        writer = csv.writer(response)

        fields = [field for field in opts.get_fields() if not \
            field.many_to_many and not field.one_to_many]

        writer.writerow([field.verbose_name for field in fields])

        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                data_row.append(value)
            writer.writerow(data_row)
        
        return response

    export_to_csv.short_description = 'Экспорт в CSV'

    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid','created', 'updated', order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]    


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']