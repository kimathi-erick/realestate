
from itertools import product
from multiprocessing import context
from tokenize import group
from urllib import request
from django.shortcuts import redirect, render
from django.http import *
from django.urls import *
from activity.decorators import unauthenticated_user

from activity.form import homesform,createuserform
from .models import *
from .form import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import homefilter,listingfilter
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json
from django.contrib.auth import get_user_model

# Create your views here.
@unauthenticated_user
def registerpage(request):   
    form=createuserform()
    if request.method == "POST":
        form = createuserform(request.POST)
        if form.is_valid():
            user=form.save()  
            
            messages.success(request,"successfully registered")
            return redirect('loginpage')
    context={
        "form":form
    } 
    return render(request,"register.html",context)   
@unauthenticated_user
def loginpage(request):   
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Username OR Password Incorrect")    
    context = {
    
    } 
    return render(request,"login.html",context)

def logoutuser(request):
    logout(request)
    return redirect('loginpage')
#@login_required(login_url='loginpage')
#admin_only
def homeactivity(request):
    
        
    homes =home.objects.all()
    myfilter= homefilter(request.GET,queryset=homes)
    homes = myfilter.qs
    homelistings = homelisting.objects.all()
    listingfilters = listingfilter(request.GET,queryset=homelistings)
    homelistings = listingfilters.qs.order_by('location')
    form = contactform()
    if request.method == "POST":
        form=contactform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")

    page=request.GET.get('page',1)
    paginator =Paginator(homelistings,9)
    try:
        homelistings=paginator.page(page)
    except PageNotAnInteger:
        homelistings = paginator.page(1)
    except EmptyPage:
        homelistings = paginator.page(paginator.num_pages)        
    context={
        "form":form,
        "homes":homes,
        "myfilter":myfilter,
        "homelistings":homelistings,
        "listingfilters":listingfilters,
    }
    return render(request,"home.html",context)

@login_required(login_url='homeactivity')
def homeretrieve(request,pk):
    homesretrieved = home.objects.get( id=pk)  
    context={
        "homesretrieved":homesretrieved
    }
    return render(request,"homesretrieved.html",context)

@login_required(login_url='homeactivity')
@allowed_users(allowed_roles=['admin'])    
def homeadding(request):
    form=homesform()
    if request.method == "POST":
        form=homesform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    context={
        "form":form
    }  
    return render(request,"homeadding.html",context)

@login_required(login_url='homeactivity') 
def homeupdate(request,pk):
    homeupdating=home.objects.get(id=pk)
    form=homesform(instance=homeupdating)
    if request.method =="POST":
        form=homesform(request.POST,instance=homeupdating,files=request.FILES)
        if form.is_valid:
            form.save()
            return redirect("/")
    context={
        "form":form
    } 
    return render(request,"formupdate.html",context) 

@login_required(login_url='homeactivity')
@allowed_users(allowed_roles=['admin'])  
def homedelete(request,pk):
    homesretrieved=home.objects.get(id=pk) 
    homesretrieved.delete()
    return redirect("/")
@login_required(login_url='homeactivity')
def listing(request):
    homelistings = homelisting.objects.all().order_by('location')
    listingfilters = listingfilter(request.GET,queryset=homelistings)
    homelistings = listingfilters.qs.order_by('location')
    page=request.GET.get('page',1)
    paginator =Paginator(homelistings,48)
    try:
        homelistings=paginator.page(page)
    except PageNotAnInteger:
        homelistings = paginator.page(1)
    except EmptyPage:
        homelistings = paginator.page(paginator.num_pages) 
    context={
        "homelistings":homelistings,
        "listingfilters":listingfilters,

    }
    return render(request,"homelisting.html",context)
@login_required(login_url='homeactivity')    
def listingretrieve(request,pk):
    retrieved= homelisting.objects.get(id=pk) 
    
    form=Scheduleviewform()
    if request.method == "POST":
        form=Scheduleviewform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listing')   
    context= {
        "retrieved":retrieved,
        "form":form
        
    }
    return render(request,"listingretrieved.html",context)


@login_required(login_url='homeactivity')
def listingcreate(request): 
    form=homelistingform()
    if request.method == "POST":
        form=homelistingform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listing')
    context={
        "form":form
    }   
    return render(request,"listingcreate.html",context)
@login_required(login_url='homeactivity')
def listingupdate(request,pk):
    retrieved = homelisting.objects.get(id=pk)
    form = homelistingform(instance=retrieved)
    if request.method == "POST":
        form = homelistingform(request.POST,files=request.FILES,instance=retrieved)
        if form.is_valid():
            form.save()
            return redirect("/")
    context ={
        "form":form
    }  
    return render(request,"listingupdate.html",context) 
@login_required(login_url='homeactivity')
@allowed_users(allowed_roles=['admin']) 
def listingdelete(request,pk):
    retrieved = homelisting.objects.get(id=pk)
    retrieved.delete()
    return redirect("/listing/")
@login_required(login_url='homeactivity')             
def userpage(request):
    context={}
    return render(request,"user.html",context)


@login_required(login_url='homeactivity')
@allowed_users(allowed_roles=['admin','customer'])
def account(request):
    customer = request.user.customer
    form =customerform(instance=customer)
    if request.method == "POST":
        form =customerform(request.POST,request.FILES,  instance=customer)
        if form.is_valid:
            form.save()
            return redirect("/listing/")
    context={
        "form":form
    }
    return render(request,"account.html",context)
@login_required(login_url='homeactivity')    
def allcustomer(request):
    allcustomers = customer.objects.all().order_by('name')
    context ={
        "allcustomers":allcustomers
    } 
    return render(request,"allcustomers.html",context) 
@login_required(login_url='homeactivity') 
@allowed_users(allowed_roles=['admin'])     
def Customerdelete(request,pk):
    customerdelete = customer.objects.get(id=pk)
    customerdelete.delete()
    return redirect("/")


"""def cart(request):
    if request.user.is_authenticated:
        Customer = request.user.customer 
        Order,created = order.objects.get_or_create(Customer=Customer,complete=False)
        items = Order.orderitem_set.all()
        
    else:
        items = []
        Order ={'get_cart_items':0,'get_cart_total':0}
        
    context={
        "Order":Order,
        "items":items
        
        
    } 
    return render(request,"cart.html",context)   

    def checkout(request):
    if request.user.is_authenticated:
        Customer = request.user.customer 
        Order,created = order.objects.get_or_create(Customer=Customer,complete=False)
        items = Order.orderitem_set.all()
        cartitems = Order.get_cart_items
        
    else:
        items = []
        Order ={'get_cart_items':0,'get_cart_total':0}
        
    context={
        "items":items,
        "Order":Order
        
    } 
    
    return render(request,"checkout.html",context)  

    def updateitem(request): 
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:',action)
    print('productId:',productId)

    Customer = request.user.customer
    product = home.objects.get(id=productId)
    Order,created = order.objects.get_or_create(Customer=Customer,complete=False)
    OrderItem, created = orderitem.objects.get_or_create(Order=Order,product=product)
    if action == 'add':
        OrderItem.quantity = (OrderItem.quantity + 1)
    elif action == 'remove':
        OrderItem.quantity = (OrderItem.quantity - 1)
    OrderItem.save()

    if OrderItem.quantity <= 0:
        OrderItem.delete()       
    return JsonResponse('item was added',safe=False)
        
"""
def like(request,pk):
    user=request.user.customer
    Home = home.objects.get(id=pk)
    current_likes = Home.likes
    liked = Likes.objects.filter(user=user,Home=Home).count()
    if not liked:
        liked = Likes.objects.create(user=user,Home=Home)
        current_likes = current_likes + 1
    else:
        liked = Likes.objects.filter(user=user,Home=Home).delete()
        current_likes = current_likes - 1
   
    Home.likes = current_likes
    Home.save()
    return HttpResponseRedirect(reverse('homeactivity'),pk)

def liking(request,pk):
    User=request.user.customer
    Homelisting = homelisting.objects.get(id=pk)
    Current_likes = Homelisting.Likes
    liked = Liking.objects.filter(User=User,Homelisting=Homelisting).count()
    if not liked:
        liked = Liking.objects.create(User=User,Homelisting=Homelisting)
        Current_likes = Current_likes + 1
    else:
        liked = Liking.objects.filter(User=User,Homelisting=Homelisting).delete()
        Current_likes = Current_likes - 1
   
    Homelisting.Likes = Current_likes
    Homelisting.save()
    return HttpResponseRedirect(reverse('listing'))  

def Notification(request):
    notifications = Scheduleview.objects.all()
    totalnotifications =notifications.count()
    messages = Contact.objects.all()
    context ={
        "notifications":notifications,
        "totalnotifications":totalnotifications,
        "messages":messages
    }
    return render(request,"notifications.html",context)
def Notificationdelete(request,pk):
    ndelete = Scheduleview.objects.get(id=pk)
    ndelete.delete()
    return redirect("/")    


    



     