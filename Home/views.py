from django.shortcuts import render,redirect
import sqlite3
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import  Paginator
from django.http import Http404,request
from django.views import generic
from django.http import JsonResponse
from django.db.models import Q
from flask import Flask, jsonify


from .filter import product_filter
from .models import Products,Customer,Order,Tags
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import authenticate_user,admin_only,for_customers  #allowed_users
# Create your views here.
from django.db.models.query import EmptyQuerySet
from .forms import *

from array import *
import stripe
stripe.api_key = "sk_test_51IDxR7A2PRoCz2JnGSo4ucTXSvY7LnzOvSxMfLOiwF02XRDY0qfHHhUt2L5e5PCLDXSNZMEAfS8lwr9c2GiHQ8ol002SXd6OOB"

@login_required(login_url='Home:login') # you are required to login to acess this page.. this would make sure that anybody who is not logged in cant access this page
#@allowed_users(allowed_roles=['Admin'])
#@admin_only

def home_view(request):

    context = {}
    return render(request,'Ecommerce-Template-Bootstrap-master/home-page.html',context)

@login_required(login_url='Home:login')
@for_customers
def customer_view(request,*args,**kwargs):
   # if not request.user.is_staff:
    #    raise Http404

    customerlist = Customer.objects.all()
    h = User.objects.all().count

    c = Customer.objects.all().order_by("phone")
    v = Customer.objects.filter(upline=request.user)
    t = Order.objects.filter(customer__name='indian')
    print(v)
    g = Customer.objects.get(user=request.user)
    order = Order.objects.filter(customer=g).order_by("-created") #.order_by("-created") is just to arrange the listof orders in descending order  you can also use -id

    #order_date = Order.objects.filter(created__lte=timezone.now())
    context = {"h":h,"g":g,'t':t,"c":c,'order':order,"customerlist":customerlist,"v":v}
    return render(request,'customer.html',context)

@login_required(login_url='Home:login')
def accountsettings_view(request,**kwargs):
    '''if request.method == 'POST':
        form = create_customer(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        context = {'form': form,'h':h,'c':c}
        return render(request, 'account_settings.html', context)'''
    b = Customer.objects.get(user=request.user)
    # g = request.user.customer     g (instance) can also be represented like this
    form = create_customer(instance=b)

    if request.method == 'POST':
        form = create_customer(request.POST, request.FILES,instance=b)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'account_settings.html', context)




@login_required(login_url='Home:login')
def about_view(request):

    context = {}
    return render(request,'about.html',context)

@authenticate_user
def signup_view(request,**kwargs):
    #if kwargs.__contains__('id'):
    if kwargs:
        print(kwargs)
        print(kwargs.__getitem__('id'))
        h = kwargs.__getitem__('id')
        d = Customer.objects.get(id=h)
        print(d)
        initial_data = {'upline': d}
        formo = create_downline(instance=d)


        form = createuserform()
        if request.method == "POST":
            form = createuserform(request.POST)
            if form.is_valid():
                form.save()
                print(form.cleaned_data)
                user = form.save()
           # print(user.username)
            #Customer.objects.create(name=user.username,user = user,email=user.email)  # with this method the Customer name wont change if the User's name is updated  it is better to use django signals
           # print(user)

                username = form.cleaned_data.get('username')
                group = Group.objects.get(name="Customers")  #Group is the user group in the admin
                user.groups.add(group)    #add form.save to a group named customer
                messages.success(request,'signup successful'+ " " + username)# it is stored as a value  no need to assign a  value to the messages. no need to pass it through context
                Customer.objects.create(name=user.username,upline=d)
                return redirect('Home:login')
    #a = form.errors
        context = {'form':form,"d":d,'formo':formo}
        return render(request,'signup.html',context)
    form = createuserform()
    if request.method == "POST":
        form = createuserform(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            user = form.save()
            # print(user.username)
            # Customer.objects.create(name=user.username,user = user,email=user.email)  # with this method the Customer name wont change if the User's name is updated  it is better to use django signals
            # print(user)

            username = form.cleaned_data.get('username')
            group = Group.objects.get(name="Customers")  # Group is the user group in the admin
            user.groups.add(group)  # add form.save to a group named customer
            messages.success(request,
                             'signup successful' + " " + username)  # it is stored as a value  no need to assign a  value to the messages. no need to pass it through context
            Customer.objects.create(user=user, name=user.username, upline='indian')
            return redirect('Home:login')
    # a = form.errors
    context = {'form': form}
    return render(request, 'signup.html', context)

@authenticate_user            #from decorator.py it also restricts a logged in user from accessimg the signup page
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = authenticate(request, username=username, password=password)
        if username is not None:  # not none    means the user name is there in database
            login(request, username)
            return redirect("Home:customer")
        else:
            messages.info(request, "Username OR Password is incorrect") #you dont need to pass through context
    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='Home:login')
def logout_view(request):
    logout(request)
    return redirect('Home:login')

@login_required(login_url='Home:login')
def try_view(request):
    products = Products.objects.all()
    print(products)
    myfilter = product_filter(request.GET, queryset=products)
    myfilt = myfilter
    context = {'myfilter': myfilt, 'products': products}
    return render(request,'try.html', context)

'''class product_view(generic.ListView):
    model = Products
    queryset =  Products.objects.all()
    paginate_by = 10
    template_name = 'Ecommerce-Template-Bootstrap-master/product-page.html'''

def product_view(request):
    productlist = Products.objects.all()



    context = {'productlist':productlist}
    return render(request,'Ecommerce-Template-Bootstrap-master/product-page.html',context)

def product_detail_view(request,id):
    product_detail = Products.objects.get(id = id)
    context = {'product_detail':product_detail}
    return render(request,"product_detail.html",context)

def javascriptt_view(request):
    mapbox_access_token = 'pk.eyJ1IjoibGVzbGV5b2x5IiwiYSI6ImNraDJpMnVieTAyYW4yeG5sOWwwM3ptaDYifQ.Eo6ubILTMV3m22AsegcqoA'
    context = {'mapbox_access_token':mapbox_access_token}
    return render(request,'javascriptt.html',context)

def add_to_cart_logic(request,id):
    items = Products.objects.get(id=id)
    print(items)
    print(request.user.customer)

    order_qs = Order.objects.filter(customer=request.user.customer,
                                     status='pending',
                                     item=items.id)
    print(order_qs)

    if order_qs:
        print('k')
        order = Order.objects.get(customer=request.user.customer,
                                  status='pending',
                                  item=items.id)

        order.quantity = order.quantity + 1
        order.save()
        print(order.quantity)
        messages.info(request, 'Item updated')
        return redirect("Home:products")
    else:
        order = Order.objects.create(customer=request.user.customer,
                                     status='pending',
                                     item_id=items.id)
        order.save()
        a = order.save()
        print(a)
        messages.info(request, 'Order created')
        return redirect("Home:products")
    addtocart = Order.objects.all()
    orders = Order.objects.filter(customer=request.user.customer,
                                     status='pending',)
    context = {'orders':orders,'addtocart':addtocart}
    return render(request,'add_to_cart.html',context)


def add_to_cart_view(request):
    addtocart = Order.objects.filter(customer=request.user.customer)
    t = 0
    for i in addtocart:
        if i.item.discount:
            a = i.saved_price()+t
            t = a
            print(t)
        else:
            v = i.item.price * i.quantity
            a = v + t
            t = a



    context = { 'addtocart': addtocart,'t':t}
    return render(request, 'add_to_cart.html', context)

def remove_cart_view(request,id):
    items = Products.objects.get(id=id)
    print(items)
    print(request.user.customer)

    order_qs = Order.objects.filter(customer=request.user.customer,
                                    status='pending',
                                    item=items.id)
    print(order_qs)

    if order_qs:
        print('k')
        order = Order.objects.get(customer=request.user.customer,
                                  status='pending',
                                  item=items.id)
        order.delete()
        messages.info(request, 'Order removed')

        return redirect('Home:products')
    messages.info(request, 'Order does not exist')
    context = {}
    return redirect('Home:products')

def reduce_cart_view(request,id):
    items = Products.objects.get(id=id)
    print(items)
    print(request.user.customer)

    order_qs = Order.objects.filter(customer=request.user.customer,
                                    status='pending',
                                    item=items.id)
    print(order_qs)

    if order_qs:
        print('k')
        order = Order.objects.get(customer=request.user.customer,
                                  status='pending',
                                  item=items.id)
        order.quantity = order.quantity - 1
        order.save()
        if order.quantity == 0:
            order.delete()
        print(order.quantity)
        messages.info(request, 'Item quantity was reduced')
        return redirect('Home:products')
    messages.info(request,'Order does not exist')
    context = {}
    return redirect('Home:products')

@login_required(login_url='Home:login')
def checkout_view (request):
    if request.method == "POST":
        print(request.POST)
    form = Checkoutform(request.POST )
    try:
        order_qs = Order.objects.filter(customer=request.user.customer,
                                        status='pending', )
        if form.is_valid():

            email = form.cleaned_data.get('email')
            Address = form.cleaned_data.get('Address')
            Address2 = form.cleaned_data.get('Address2')
            country = form.cleaned_data.get('country')
            state = form.cleaned_data.get('state')
            Zip = form.cleaned_data.get('Zip')
            Shipping_Address = form.cleaned_data.get('Shipping_Address')
            payment_options =  form.cleaned_data.get('payment_options')
            billing_address = Checkout.objects.create(user= request.user,
                                       Email = email,
                                       Address= Address,
                                       Address2= Address2,
                                       Country= country,
                                       state= state,
                                       Zip= Zip,
                                       Shipping_Address=Shipping_Address,
                                         Payment_options=payment_options,
                                       )
            print(billing_address.Payment_options)



            for obj in order_qs:
                print(obj.Billing_address)
                obj.Billing_address = billing_address
                obj.save()
            return redirect(billing_address.paymenturl())
        else:
            print('kj')
    except ObjectDoesNotExist:
        messages.error(request,'you dont have an order')

    addtocart = Order.objects.filter(customer=request.user.customer)
    t = 0
    for i in addtocart:
        if i.item.discount:
            a = i.saved_price() + t
            t = a
            print(t)
        else:
            v = i.item.price * i.quantity
            a = v + t
            t = a


    context = {'form':form,'addtocart': addtocart, 't': t}
    return render(request,'Ecommerce-Template-Bootstrap-master/checkout-page.html',context)

def payment_view (request,id):
    # Set your secret key. Remember to switch to your live secret key in production!
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = 'sk_test_51IDxR7A2PRoCz2JnGSo4ucTXSvY7LnzOvSxMfLOiwF02XRDY0qfHHhUt2L5e5PCLDXSNZMEAfS8lwr9c2GiHQ8ol002SXd6OOB'

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 2000,
                        'product_data': {
                            'name': 'Stubborn Attachments',
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= request.build_absolute_url(reverse('success')) + '/success.html',
            cancel_url= request.build_absolute_url(reverse('success')) + '/cancel.html',
        )

        context = {'id': checkout_session.id}
        return render(request,'payment.html',context)
    except :
       
        context = {}
        return render(request,'payment.html',context)


if __name__ == '__main__':
    app.run(port=4242)

def success (request):
    context = {}
    return render(request, 'success.html', context)

def cancel (request):
    context = {}
    return render(request, 'cancel.html', context)

 #  if order_qs.exists:
  #      order = Order.objects.get(customer=request.user.customer,
   #                                  status='pending',
    #                                 item=items.id)
     #   order.quantity +=1
    #else:
     #   order = Order.objects.create(customer=request.user.customer,
      #                               status='pending',
       #                              item_id=items.id)
        #print(order)
'''
    if order_qs.none:
        order = Order.objects.create(customer=request.user.customer,
                                     status='pending',
                                     item_id=items.id)
        order.save()
        a = order.save()
        print(a)
        return redirect("Home:products")
    else:
        if order_qs.exists :
            order = Order.objects.get(customer=request.user.customer,
                                     status='pending',
                                     item=items.title)

            order.quantity = order.quantity + 1

            print(order.quantity)
            return redirect("Home:products")
'''