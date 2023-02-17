from dataclasses import fields
from xml.parsers.expat import model
from django.forms import ModelForm,DateInput
from django.forms.fields import *
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .widgets import *



class homesform(ModelForm):

    class Meta:
        model=home
        fields={
            "Hometype",
            "Price",
            "Location",
            "Image",
            "Bathrooms",
            "Bedrooms", 
            "Sqr_footage",
            "Agent_no",
            "category",
            "Text"
        }

class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class homelistingform(ModelForm):

    class Meta:
        model=homelisting
        fields={
            "category",
            "hometype",
            "bedrooms",
            "bathrooms",
            "sqr_footage",
            "location" ,
            "agent_no" ,
            "image",
            "price",
            "text"
        }

class customerform(ModelForm):
    class Meta:
        model = customer
        fields = '__all__'
        exclude = ['user']

      

class contactform(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__' 

class dateinput(forms.DateInput):
    input_type = 'date'
class timeinput(forms.TimeInput):
    input_type = 'time'    


class Scheduleviewform(ModelForm):
    Text = forms.CharField(widget = forms.Textarea(attrs={'placeholder':'I am intrested'}))
    Email = forms.EmailField(widget = forms.EmailInput(attrs={'placeholder':'you@gmail.com'}))
    class Meta:
        
        model = Scheduleview
        fields = '__all__'
        widgets = {'Date':dateinput(),'Time':timeinput()}
        
