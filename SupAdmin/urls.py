from django.urls import path
from .views import (addcategory,updateCategory,
                    deleteCategory,addproduct,category_product_view,
                    order_view,updateOrderStatus,updateProduct,deleteProduct)


urlpatterns = [
    path('addcategory/',addcategory,name='addcategory'),
    path('updateCategory/<int:id>/',updateCategory,name='updateCategory'),
    path('deleteCategory/<int:id>/',deleteCategory,name='deleteCategory'),
    path('addproduct/',addproduct,name='addproduct'),
    path('updateProduct/<int:id>/',updateProduct,name='updateProduct'),
    path('deleteProduct/<int:id>/',deleteProduct,name='deleteProduct'),
    path('catAndprod/',category_product_view,name='catAndprod'),
    path('orderview/',order_view,name='orderview'),
    path('updateOrderStatus/<int:id>/',updateOrderStatus,name='updateOrderStatus'),
]