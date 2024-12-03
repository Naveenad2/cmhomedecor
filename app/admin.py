# admin.py
from django.contrib import admin
from .models import *
from .models import Service, ServiceOption
from .models import Product, ProductFeature, CustomizationOption

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discounted_price', 'in_stock', 'is_new', 'made_to_order')

@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')

@admin.register(CustomizationOption)
class CustomizationOptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'choices')

class ServiceOptionInline(admin.TabularInline):
    model = ServiceOption
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    inlines = [ServiceOptionInline]

admin.site.register(Service, ServiceAdmin)

admin.site.register(ContactInfo)
admin.site.register(SocialMedia)
admin.site.register(SiteLogo)
admin.site.register(Banner)
admin.site.register(FunFact)
admin.site.register(VideoSection)

