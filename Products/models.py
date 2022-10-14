from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_info(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=False,null=False)
    GENDER_CHOICE= (('M','Male'),('F','Female'),('OG','Other'))
    profile_pic = models.ImageField(upload_to='profilepic',blank=False,null=False)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICE,blank=False,null=False)
    address = models.CharField(max_length=100,blank=False,null=False)
    phone = models.CharField(max_length=15,blank=False,null=False)

    def __str__(self):
        return "User: {},Genger: {}".format(self.user.first_name, self.gender)



class Category(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)    
    

    def __str__(self):
        return self.name


    @staticmethod
    def get_all_category():
        return Category.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    unit = models.CharField(max_length = 15,blank=True)
    description = models.TextField(max_length=1000,null=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to = 'products/')


    def __str__(self):
        return self.name

    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(categoryid):
        if categoryid:
            return Product.objects.filter(category = categoryid)
        else:
            return Product.objects.all()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    bkashTrxID = models.CharField(max_length=150,default='',blank=True)
    address = models.CharField(max_length=150,default='')
    phone = models.CharField(max_length=15,default='')
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
    
    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(user = customer_id).order_by('-id')
    
