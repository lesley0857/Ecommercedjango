from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
from .views import signup_view

'''@receiver(post_save,sender=User)
def create_customer(sender,instance,created,**kwargs):
    if created:
        Customer.objects.create(user=instance,name=instance.username,upline=signup_view.d)
        print("Customer created")'''

'''@receiver(post_save,sender=User)
def create_upline(sender,instance,created,**kwargs):
    if created:
        Upline.objects.create(upline=instance.username)
        print("upline created")
'''

#post_save.connect(create_customer,sender=User)

'''@receiver(post_save,sender=User)
def update_customer(sender,instance,created,**kwargs):
    if created == False:
        instance.customer.save()
        print("Customer updated")
        '''

#post_save.connect(update_customer,sender=User)  #connect the signal this way or use RECIEVER DECORATOR