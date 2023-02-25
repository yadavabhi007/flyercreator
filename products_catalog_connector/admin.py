from django.contrib import admin
from products_catalog_connector.models import Distribution, Product, Picture, Seller, Category, Subcategory

admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Picture)



class ProductAdmin(admin.ModelAdmin):
    model = Product
    fields = ('category',)

admin.site.register(Product, ProductAdmin)

class DistributionAdmin(admin.ModelAdmin):
    model = Distribution
    fields = ('product', 'seller', 'code')
    readonly_fields = ['product', 'seller', 'code']
    list_filter = ('seller', )

admin.site.register(Distribution, DistributionAdmin)