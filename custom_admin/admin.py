from django.contrib import admin

from .models import User,Category,ProductAttribute,ProductAttributeValues,Product,ProductImage

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValues)
