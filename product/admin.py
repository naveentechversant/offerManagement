from django.contrib import admin
import models

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code','name','stock','created_date','price')
    fields = ('code','name','stock','price')
admin.site.register(models.Product, ProductAdmin)

class OfferAdmin(admin.ModelAdmin):
	list_display = ('code','start','end','discount','type_of_discount')
	fields = ('code','start','end','discount','type_of_discount')

admin.site.register(models.Offers, OfferAdmin)