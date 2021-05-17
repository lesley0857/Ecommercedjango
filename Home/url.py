from django.urls import path
from Home.views import *
from .models import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


app_name = "Home"
urlpatterns = [
    path('home/',home_view,name='home'),
    path('', product_view, name='products'),
    path('productdetail/<int:id>/', product_detail_view, name='productdetail'),
    path('about/', about_view, name='about'),
    path('customer/', customer_view, name='customer'),
    path('customer/<int:id>/', signup_view, name='customer_ref'),
    path('try/', try_view, name='try'),
    path('javascriptt/', javascriptt_view, name='javascriptt'),
    path('logout/', logout_view, name='logout'),
    path('addtocart/<int:id>/', add_to_cart_logic, name='addtocartlogic'),
    path('removecartt/<int:id>/', remove_cart_view, name='removecart'),
    path('reducecartt/<int:id>/', reduce_cart_view, name='reducecart'),
    path('addtocart/', add_to_cart_view, name='addtocartt'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/<str:id>', payment_view, name='payment'),
    path('acctsetting/', accountsettings_view, name='acctsetting'),
    path('home/',home_view,name='home'),
    path('cancel/', cancel, name='cancel'),
    path('success/', success, name='success'),
    ]