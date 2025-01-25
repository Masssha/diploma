from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Shop, Category, Person, Product, Parameter, ProductInfo, ProductParameter, Contact, Order, OrderItem, ConfirmEmailToken


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # pass
    list_display = ('name', )
    list_filter = ('name', )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
# class CustomUserAdmin(UserAdmin):
    # model = Person
    #
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Personal info', {'fields': ('first_name', 'last_name')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )
    # that's what I still didn't know...
    list_display = ('first_name', 'last_name', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'model')
    list_filter = ('name', 'category')


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'shop', 'quantity', 'price', 'price_rrc')
    list_filter = ('product', 'shop', 'quantity', 'price', 'price_rrc')


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('parameter_name', )
    list_filter = ('parameter_name', )


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ('product_info', 'parameter', 'parameter_value')
    list_filter = ('product_info', 'parameter', 'parameter_value')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'house', 'phone')
    list_filter = ('user', 'city')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'order_dt', 'contact')
    list_filter = ('user', 'state', 'order_dt', 'contact')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'shop')
    list_filter = ('order', 'product', 'quantity', 'shop')

@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)




