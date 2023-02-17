
import datetime
from distutils.command.upload import upload
import email
from email.policy import default
from operator import mod
import profile
from tkinter import CASCADE
from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from django.db.models import Avg
from datetime import datetime


# Create your models here.
LOCATION_CHOICES = (
        ("Naivasha","Naivasha"),
        ("Molo","Molo"),
        ("Gilgil","Gilgil"),
        ("Njoro","Njoro"),
        ("Maai Mahiu","Maai Mahiu"),
        ("Subukia","Subukia"),
        ("Dundori","Dundori"),
        ("Salgaa","Salgaa"),
        ("Mau Narok","Mau Narok"),
        ("Bahati","Bahati"),
        ("Rongai","Rongai"),
        ("Olenguruone","Olenguruone")

    )
PRICE_CHOICES = (
        ("1000.00","1000.00"),
        ("2000.00","2000.00"),
        ("3000.00","3000.00"),
        ("4000.00","4000.00"),
        ("5000.00","5000.00"),
        ("6000.00","6000.00"),
        ("7000.00","7000.00"),
        ("8000.00","8000.00"),
        ("9000.00","9000.00")
    )
CATEGORY_CHOICES=(
        ("FOR SALE","FOR SALE"),
        ("FOR RENT","FOR RENT")
    )        
class home(models.Model):
    Hometype=models.CharField(max_length=100,null=True)
    Price=models.CharField(max_length=20,choices=PRICE_CHOICES)
    Location=models.CharField(max_length=100,choices=LOCATION_CHOICES)
    Image=models.ImageField()
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES,null=True)
    Bathrooms = models.IntegerField(null=True)
    Bedrooms = models.IntegerField(null=True)
    Sqr_footage = models.FloatField(null=True)
    Agent_no = PhoneField(null=True)
    likes = models.IntegerField(default=0)
    Text = models.TextField(max_length=200,null=True,blank=True)
    

    def __str__(self):
        return self.Hometype

    @property
    def ImageURL(self):
        try:
            url= self.Image.url
        except:
            url = ''
        return url     

class homelisting(models.Model):
    PRICE_CHOICES = (
        ("1000.00","1000.00"),
        ("2000.00","2000.00"),
        ("3000.00","3000.00"),
        ("4000.00","4000.00"),
        ("5000.00","5000.00"),
        ("6000.00","6000.00"),
        ("7000.00","7000.00"),
        ("8000.00","8000.00"),
        ("9000.00","9000.00")
    )
    LOCATION_CHOICES = (
        ("Naivasha","Naivasha"),
        ("Molo","Molo"),
        ("Gilgil","Gilgil"),
        ("Njoro","Njoro"),
        ("Maai Mahiu","Maai Mahiu"),
        ("Subukia","Subukia"),
        ("Dundori","Dundori"),
        ("Salgaa","Salgaa"),
        ("Mau Narok","Mau Narok"),
        ("Bahati","Bahati"),
        ("Rongai","Rongai"),
        ("Olenguruone","Olenguruone")

    )
    CATEGORY_CHOICES=(
        ("FOR SALE","FOR SALE"),
        ("FOR RENT","FOR RENT")
    )
    HOME_CHOICES = (
        ("Land for sale","Land for sale"),
        ("Apartment","Apartment"),
        ("Bedsitter","Bedsitter"),
        ("Office","Office"),
        ("villa","villa"),
        ("Townhouse","Townhouse"),
        ("Single room","Single room"),
    )

    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES,null=True,blank=True)
    hometype = models.CharField(max_length=20,choices=HOME_CHOICES,null=True,blank=True)
    bedrooms = models.IntegerField(null=True,blank=True)
    price = models.CharField(max_length=20,choices=PRICE_CHOICES)
    sqr_footage = models.FloatField(null=True,blank=True)
    location = models.CharField(max_length=50,choices=LOCATION_CHOICES)
    agent_no = PhoneField(null=True,blank=True)
    bathrooms = models.IntegerField(null=True,blank=True)
    image = models.ImageField()
    Likes = models.IntegerField(default=0)
    text = models.TextField(max_length=1000,null=True,blank=True)
    def __str__(self):
        return self.hometype

class customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=20)
    phone = PhoneField()
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    profile_pic = models.ImageField(default='default.jpg',upload_to = 'profile_pics')
    def __str__(self):
        return str(self.user)
 
"""class order(models.Model):
    Customer = models.ForeignKey(customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total  

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total              

class orderitem(models.Model):
    product = models.ForeignKey(home,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=0)
    Order = models.ForeignKey(order,on_delete=models.SET_NULL,null=True,blank=True)

    @property
    def get_total(self):
        total = self.product.Price * self.quantity
        return total
"""    


class Likes(models.Model):
    user = models.ForeignKey(customer,on_delete=models.CASCADE,related_name="user_likes") 
    Home = models.ForeignKey(home,on_delete=models.CASCADE,related_name="home_likes")

class Liking(models.Model):
    User = models.ForeignKey(customer,on_delete=models.CASCADE,related_name="User_likes") 
    Homelisting = models.ForeignKey(homelisting,on_delete=models.CASCADE,related_name="Home_likes")
class Contact(models.Model) :
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    text = models.TextField(max_length= 500)

    def __str__(self):
        return self.email 

class Scheduleview(models.Model) :
    Name = models.CharField(max_length=100)
    Phone = models.CharField(max_length=10)
    Date = models.DateField()
    Time = models.TimeField(null=True)
    Email = models.EmailField()
    Location = models.CharField(max_length = 50)
    Text = models.TextField(max_length= 500)
    

    def __str__(self):
        return self.email      








