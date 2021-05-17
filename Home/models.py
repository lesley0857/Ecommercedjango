from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.http import Http404,request
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.




class Customer(models.Model):
    PLANS = (('Diamond','Diamond'),('Gold','Gold'),('Silver','Silver'))
    user = models.OneToOneField(User,null = True,on_delete = models.CASCADE,default=True)
    name  = models.CharField(null=True,max_length=200)
    upline= models.CharField(null=True, max_length=200)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    created = models.DateTimeField(null=True,auto_now=False,auto_now_add=True)
    address = models.TextField(null=True)
    plans = models.CharField(max_length=200,choices=PLANS,default= 'PLANS[0]')
    profile_pic = models.ImageField(default="/Koala.jpg/")
    content = models.FileField(upload_to='images')
    def __str__(self):
        return str(self.user)



    def get_absolute_url(self):
        return reverse('Home:customer')

    def get_ref_link(self):
        return reverse('Home:customer_ref',kwargs={"id":self.id})

    def about_get_absolute_url(self):
        return reverse('Home:about')







class Downline(models.Model):
    downline = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)





class Tags(models.Model):
    name = models.CharField(null=True,max_length=200)
    def __str__(self):
        return self.name

class Products(models.Model):
    title  = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    description = models.TextField(null=True,blank=True)
    tag  = models.ManyToManyField(Tags)
    profile_pic = models.ImageField(null=True,blank=True,default="/Koala.jpg/")
    discount =  models.FloatField(blank=True,null=True)

    def get_absolute_url(self):
        return reverse('Home:productdetail',kwargs={"id":self.id})

    def get_addtocart_url(self):
        return reverse('Home:addtocartlogic', kwargs={"id": self.id})

    def get_removecart_url(self):
        return reverse('Home:removecart', kwargs={"id": self.id})

    def get_reducecart_url(self):
        return reverse('Home:reducecart', kwargs={"id": self.id})

    def __str__(self):
        return self.title

class Checkout(models.Model):
    user = models.ForeignKey(User,null = True,on_delete = models.CASCADE,default=True)
    Email = models.EmailField()
    Address = models.CharField(max_length=200,null=True)
    Address2 = models.CharField(max_length=200, null=True,blank=False)
    Country = CountryField(multiple=False)
    state = models.CharField(max_length=200, null=True,blank=False)
    Zip = models.CharField(max_length=200, null=True)
    Shipping_Address = models.CharField(max_length=200, null=True,blank=False)
    Payment_options = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.user.username

    def paymenturl(self):
        return reverse('Home:payment', kwargs={"id": self.Payment_options})


class Order(models.Model):
    STATUS = (('delivered','delivered'),('pending','pending'),('out for delivery','out for delivery'))
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    item = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True,default=1)
    status  = models.CharField(max_length=200,choices=STATUS)
    created = models.DateTimeField(null=True, auto_now=False, auto_now_add=True)
    Billing_address = models.ForeignKey(
          Checkout,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.customer.user.username
    def get_reducecart_url(self):
        return reverse('Home:reducecart', kwargs={"id": self.id})

    def realprice(self):
        if self.item.discount:
            j =self.item.price - self.item.discount
            return j * self.quantity
        return self.item.price * self.quantity

    def saved_price(self):
        if self.item.discount:
            v = self.realprice() - self.item.discount
            return v
        return self.realprice()


COUNTRIES = (('I','India'),('G','Ghana'))


class OrderItem(models.Model):
    item = models.ForeignKey(Products,null=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True)

'''class Plans(models.Model):
    name = models.CharField(null=True,max_length=200)
    def __str__(self):
        return self.name'''