from django.urls import path
from .views import (Shop,product_details,SignUp,signinView,
                    user_profile,editUserInfo,signoutView,
                    Cart,Checkout,IncDec,ProductSearch)


urlpatterns = [
    path('',Shop.as_view(),name='home'),
    path('signup/',SignUp,name='signup'),
    path('signin/',signinView,name='signin'),
    path('userprofile/',user_profile,name='userprofile'),
    path('editUserInfo/',editUserInfo,name='editUserInfo'),
    path('signout/',signoutView,name='signout'),
    path('productdetail/<int:id>/',product_details,name='productdetail'),
    path('cart/',Cart.as_view(),name='cart'),
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('incdec/',IncDec.as_view(),name='incdec'),
    path('ProductSearch/',ProductSearch.as_view(),name='ProductSearch'),
]