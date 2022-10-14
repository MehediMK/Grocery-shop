from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.views import View
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Category,Product,User_info,Order
from .forms import (CreateUserForm,UserInfoForm,UserLoginForm,UserFLEname)
from django.contrib.auth.models import User


def SignUp(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        form1 = UserInfoForm(request.POST,request.FILES or None)

        if form.is_valid() and form1.is_valid():
            newuser = form.save()
            newuserinfo = form1.save(commit=False)
            newuserinfo.user = newuser
            newuserinfo.save()
            return redirect('signin')
        
    else:
        form = CreateUserForm()
        form1 = UserInfoForm()
        
    context = {
        'form':form,
        'form1':form1,
    }
    return render(request,'accounts/signup.html',context)

def signinView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username , password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
    else:
        form = UserLoginForm()
    
    context = {
        'form':form,
    }
    return render(request,'accounts/signin.html',context)

@login_required(redirect_field_name='signin')
def user_profile(request):
    context = {}
    user = request.user
    orders = Order.get_orders_by_customer(user)
    # get user
    get_user = User_info.objects.get(user__id=user.id)
    
    # category,product,revenew area start
    if request.user.is_superuser:
        # total price count
        revenew = Order.objects.all()
        revenewsum = 0
        for rev in revenew:
            if rev.status == True:
                revenewsum+=rev.price
        #end revenew total price

        context['revenewsum']=revenewsum #pagination done
    
        # end category,product,revenew area
    

    context['user'] =user
    context['profile'] =get_user
    context['orders'] =orders
    
    return render(request,'userprofile.html',context)


@login_required(redirect_field_name='login')
def editUserInfo(request):
    if request.method == 'POST':
        mydata = User_info.objects.get(user=request.user)
        user = User.objects.get(username=request.user.username)
        form = UserInfoForm( request.POST, request.FILES or None, instance=mydata)
        form1 = UserFLEname( request.POST, request.FILES or None, instance=user)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
        return redirect('userprofile')
    else:
        mydata = User_info.objects.get(user=request.user)
        user = User.objects.get(username=request.user.username)
        form = UserInfoForm(instance=mydata)
        form1 = UserFLEname(instance=user)
    context={
        'form':form,
        'form1':form1,
    }
    return render(request,'editinfo.html',context)

def signoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('signin')

class Shop(View):
    def get(self,request):
        product_list = None
        categoryID = request.GET.get('category')
        if categoryID:
            product_list = Product.objects.filter(category__id=categoryID)
        else:
            product_list = Product.objects.all()
        all_category = Category.objects.all()

        # this query for pagination
        productview = request.GET.get('productview', 1)
        home_paginator = Paginator(product_list, 12)
        try:
            products_list = home_paginator.page(productview)
        except PageNotAnInteger:
            products_list = home_paginator.page(1)
        except EmptyPage:
            products_list = home_paginator.page(home_paginator.num_pages)
        # end pagination query

        context = {
            'products':products_list,
            'categories':all_category,
        }
        return render(request,'index.html',context)
    def post(self,request):
        product = request.POST.get('productid')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            item = cart.get(product)
            if item:
                if remove:
                    if item<=1:
                        cart.pop(product)
                    else:
                        cart[product] = item-1
                else:
                    cart[product] = item+1
            else:
                cart[product] = 1
        
        else:
            cart = {}
            cart[product] = 1
        
        request.session['cart'] = cart

        product_list = Product.objects.all()
        print('product:',request.session.get('cart'))
        return redirect('home')


def product_details(request,id):
    product = get_object_or_404(Product,id=id)
    return render(request,'productDetail.html',{'product':product})

class ProductSearch(View):
    def get(self,request):  
        context = {}  
        mysearch = request.GET.get('search')
        context['mysearch'] = mysearch

        products = None

        categories = Category.objects.all()
        context['categories'] = categories

        categoryID = request.GET.get('category')
        message = None
        # here get product by search name
        if mysearch:
            myproductsearch = Product.objects.filter(name__icontains=mysearch)
            if myproductsearch:
                products=myproductsearch
            else:
                message = 'Search not found'
        else:
            if categoryID:
                products = Product.objects.filter(category__id=categoryID)
            else:
                products = Product.objects.all()
        # here check froduct or not th
        if message:
            context['message'] = message
        else:
            
            # this query for pagination
            productview = request.GET.get('productview', 1)
            home_paginator = Paginator(products, 12)
            try:
                products_list = home_paginator.page(productview)
                context['products'] = products_list
            except PageNotAnInteger:
                products_list = home_paginator.page(1)
                context['products'] = products_list
            except EmptyPage:
                products_list = home_paginator.page(home_paginator.num_pages)
                context['products'] = products_list
            # end pagination query

        return render(request,'index.html',context)

class Cart(View):
    def get(self,request):
        mycart = request.session.get('cart')
        if mycart:
            ids = list(request.session.get('cart').keys())
            products = Product.get_product_by_id(ids)
            return render(request,'cart.html',{'products':products})
        else:
            request.session['cart'] = {}
            ids = list(request.session.get('cart').keys())
            products = Product.get_product_by_id(ids)
            return render(request,'cart.html',{'products':products})

class IncDec(View):
    def post(self,request):
        product = request.POST.get('productid')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('cart')


class Checkout(View):
    def post(self,request):
        address = request.POST.get('address')
        bkashtrxid = request.POST.get('bkashtrxid')
        phone = request.POST.get('phone')
        user = request.user
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        print(address, phone, user, cart, products,bkashtrxid)

        for product in products:
            # print(cart.get(str(product.id)))
            order = Order(user=user,
                          product=product,
                          price=product.price,
                          bkashTrxID=bkashtrxid,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
            print(user,product,product.price,address,phone,cart.get(str(product.id)),bkashtrxid)
        request.session['cart'] = {}

        return redirect('cart')


