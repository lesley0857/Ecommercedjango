from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
def authenticate_user(view):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated :  # this would make sure that you cant goto signup page while u are signed in
            return redirect('Home:customer')
        else:  # if u are not signed in then you can acces the signup page
            return view(request,*args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():              #if a group of users exists
                group = request.user.groups.all()[0].name      # group = the first group in the list[] of groups
            if group in allowed_roles:                      # if the first group in the group list is in the allowed roles
                return view_func(request,*args,**kwargs)
            else:                                              # if the first group in the group list is not in the allowed roles
                return HttpResponse('You are not authorized')
        return wrapper_func   # while returning a function do not add brackets
    return decorator

def admin_only(view_func):
    def wraper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'Customers':
            return redirect('Home:customer')
        if group == 'Admin':
            return view_func(request,*args,**kwargs)
    return wraper_func

def for_customers(view_func):
    def wraper_func(request,*args,**kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'Admin':
            return view_func(request,*args,**kwargs)
        else:
            return view_func(request,*args,**kwargs)
    return wraper_func

