from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from django.forms import ModelForm
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import *
from .views import *
class createuserform(UserCreationForm): #for registering a user

    class Meta:
        model = User
        fields = ['username','email','password1','password2']




class create_customer(forms.ModelForm):
    created = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Customer
        fields ='__all__'
        exclude = ['user']

    def phone_valid(self,request,*args,**kwargs):
        phone =self.cleaned_data.get("phone")
        if "9" in phone:
            print(phone)
        else:
            pass

"""class create_upline(forms.ModelForm):
    upline = forms.CharField(widget=forms.TextInput)
    class Meta:
        model =Upline
        fields =['upline'] """

class create_downline(forms.ModelForm):

    class Meta:
        model = Downline
        fields ='__all__'


PAYMENT_CHOICES = (('S','Stripe'),('P','Paypal'))

class Checkoutform(forms.Form):

    email = forms.EmailField()

    Address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    Address2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget())
    state = forms.ChoiceField(required=False)
    Zip = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    Shipping_Address = forms.CharField(widget=forms.CheckboxInput())
    payment_options = forms.ChoiceField(widget=forms.RadioSelect,
                                        choices=PAYMENT_CHOICES)






class Payment_form(forms.Form):


    name_on_card = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control'} ))

    credit_card_number = forms.IntegerField()
    Expiration = forms.DateField()
    CVV = forms.IntegerField()





