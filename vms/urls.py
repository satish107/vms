"""vms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from orders.views import home
from orders.urls import urlpatterns as order_urlpatterns
from vendors.urls import urlpatterns as vendor_urlpatterns
from auth.urls import urlpatterns as auth_urlpatterns

urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
]

urlpatterns += order_urlpatterns
urlpatterns += vendor_urlpatterns
urlpatterns += auth_urlpatterns