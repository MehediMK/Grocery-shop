from django.contrib import admin
from .models import User_info,Category,Product,Order
from import_export.admin import ImportExportModelAdmin

class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	fields=['name', 'price', 'unit', 'description', 'category', 'image']
	list_display=['id','name','category','price','image']

	
class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	fields=['name']
	list_display=['id','name']


# Register your models here.
admin.site.register(User_info)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
