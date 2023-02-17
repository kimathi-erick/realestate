"""realestate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from unicodedata import name
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from activity.views import  *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeactivity, name='homeactivity'),
    path('register/', registerpage, name='registerpage'),
    path('login/', loginpage, name='loginpage'),
    path('logout/', logoutuser, name='logoutuser'),
    path('notification/', Notification, name='Notification'),
    path('user/', userpage, name='userpage'),
    #path('cart/', cart, name='cart'),
    #path('checkout/', checkout, name='checkout'),
    path('account/', account, name='account'),
    path('homeadding/', homeadding, name='homeadding'),
    path('retrieve/<pk>/', homeretrieve ,name='homeretrieve'),
    path('retrieve/<pk>/like', like,name='like'),
    path('retrieve/<pk>/update/', homeupdate, name='homeupdate'),
    path('retrieve/<pk>/delete/', homedelete, name='homedelete'),
    path('listing/', listing, name='listing'),
    path('listingcreate/', listingcreate, name='listingcreate'),
    path('retrieves/<pk>/', listingretrieve ,name='listingretrieve'),
    path('retrieves/<pk>/liking', liking ,name='liking'),
    path('retrieves/<pk>/update/',listingupdate, name='listingupdate'),
    path('retrieves/<pk>/delete/',listingdelete, name='listingdelete'),
    path('customerdelete/<pk>/delete/',Customerdelete, name='Customerdelete'),
    path('ndelete/<pk>/delete/',Notificationdelete, name='Notificationdelete'),
    #path('updateitem/', updateitem, name='updateitem'),
    path('allcustomer/',allcustomer,name='allcustomer')
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
