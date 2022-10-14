from django import forms
from django.contrib.auth.models import User
from Products.models import User_info,Category,Product,Order


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)


    