from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from Products.models import Category,Product,User_info,Order
from .forms import (AddCategoryForm,AddProductForm,UpdateOrderStatusForm)
from django.contrib.auth.models import User


@login_required(redirect_field_name='signin')
def addcategory(request):
    if request.method=='POST':
        if request.user.is_superuser:
            form = AddCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('userprofile')
            else:
                return redirect('addcategory')
        else:
            return redirect('userprofile')
    else:
        if request.user.is_superuser:
            form = AddCategoryForm()
        else:
            return redirect('userprofile')
    context = {
        'form':form,
    }
    return render(request,'addcategory.html',context)


@login_required(redirect_field_name='signin')
def addproduct(request):
    if request.method=='POST':
        if request.user.is_superuser:
            form = AddProductForm(request.POST,request.FILES or None)
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                return redirect('addproduct')
        else:
            return redirect('userprofile')
    else:
        if request.user.is_superuser:
            form = AddProductForm()
        else:
            return redirect('userprofile')
    context = {
        'form':form,
    }
    return render(request,'addproduct.html',context)


@login_required(redirect_field_name='signin')
def category_product_view(request):
    context = {}
        
    # category,product,revenew area start
    if request.user.is_superuser:
        
        # this query for category
        categorys = Category.objects.all()
        category_page = request.GET.get('categorypage', 1)
        category_paginator = Paginator(categorys, 5)
        try:
            category_list = category_paginator.page(category_page)
        except PageNotAnInteger:
            category_list = category_paginator.page(1)
        except EmptyPage:
            category_list = category_paginator.page(category_paginator.num_pages)
        
        context['categorys']=category_list


        # this query for products
        products = Product.objects.all()       
        page1 = request.GET.get('page', 1)
        paginator = Paginator(products, 5)
        try:
            products_list = paginator.page(page1)
        except PageNotAnInteger:
            products_list = paginator.page(1)
        except EmptyPage:
            products_list = paginator.page(paginator.num_pages)
        
        context['products']=products_list
    else:
        return redirect('userprofile')
        
    return render(request,'catprod.html',context)




@login_required(redirect_field_name='signin')
def order_view(request):
    context = {}
        
    # category,product,revenew area start
    if request.user.is_superuser:
        # this query for order
        myorders = Order.objects.all()
        order_page = request.GET.get('orderpage', 1)
        order_paginator = Paginator(myorders, 5)
        try:
            order_list = order_paginator.page(order_page)
        except PageNotAnInteger:
            order_list = order_paginator.page(1)
        except EmptyPage:
            order_list = order_paginator.page(order_paginator.num_pages)

               
        context['orders']=order_list
    else:
        return redirect('userprofile')
        
        
    return render(request,'orderview.html',context)


@login_required(redirect_field_name='signin')
def updateProduct(request,id):
    context = {}
    if request.method == 'POST':
        if request.user.is_superuser:
            mydata = Product.objects.get(pk=id)
            
            form = AddProductForm( request.POST,request.FILES or None, instance=mydata)
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                return redirect('catAndprod')
        else:
            return redirect('userprofile')
    else:
        if request.user.is_superuser:
            mydata = Product.objects.get(id=id)
            form = AddProductForm(instance=mydata)
            context['form']=form
        else:
            return redirect('userprofile')

    return render(request,'updateproduct.html',context)

@login_required(redirect_field_name='signin')
def deleteProduct(request,id):
    if request.user.is_superuser:
        Product.objects.get(pk=id).delete()
        return redirect('catAndprod')
    else:
        return redirect('userprofile')

@login_required(redirect_field_name='signin')
def updateCategory(request,id):
    context = {}
    if request.method == 'POST':
        if request.user.is_superuser:
            mydata = Category.objects.get(pk=id)
            
            form = AddCategoryForm( request.POST,instance=mydata)
            if form.is_valid():
                form.save()
                return redirect('catAndprod')
            else:
                return redirect('catAndprod')
        else:
            return redirect('userprofile')
    else:
        if request.user.is_superuser:
            mydata = Category.objects.get(id=id)
            form = AddCategoryForm(instance=mydata)
            context['form']=form
        else:
            return redirect('userprofile')

    return render(request,'updateCategory.html',context)

@login_required(redirect_field_name='signin')
def deleteCategory(request,id):
    if request.user.is_superuser:
        Category.objects.get(pk=id).delete()
        return redirect('catAndprod')
    else:
        return redirect('userprofile')


@login_required(redirect_field_name='signin')
def updateOrderStatus(request,id):
    context = {}
    if request.method == 'POST':
        if request.user.is_superuser:
            mydata = Order.objects.get(pk=id)
            
            form = UpdateOrderStatusForm( request.POST,instance=mydata)
            if form.is_valid():
                form.save()
                return redirect('orderview')
            else:
                return redirect('orderview')
        else:
            return redirect('userprofile')
    else:
        if request.user.is_superuser:
            mydata = Order.objects.get(id=id)
            form = UpdateOrderStatusForm(instance=mydata)
            context['form']=form
            context['message']="Order Status"

        else:
            return redirect('userprofile')

    return render(request,'updateCategory.html',context)

