from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    def not_avialable(self, request, queryset):
        for obj in queryset:
            obj.not_avialable()
            self.message_user(request, f'Товара {obj.name} нет в наличии')
    not_avialable.short_description = 'Товара нет в наличии'

    def on_avialable(self, request, queryset):
        for obj in queryset:
            obj.on_avialable()
            self.message_user(request, f'Товара {obj.name} в наличии')
    # on_avialable.short_description = 'Товар в наличии'

    list_display = ('name', 'slug', 'category', 'price', 'available', 'image', 'created', 'updated')
    list_filter = ('category', 'available', 'created', 'updated')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}
    actions = [not_avialable, on_avialable]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
