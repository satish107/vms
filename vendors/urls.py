from django.urls import path, include
from django.contrib import admin

from vendors import controllers as vendor_views

urlpatterns = [
    path("api/<int:version>/vendors", vendor_views.VendorViewAPI.as_view(), name="vendors.vendor-list"),
    path("api/<int:version>/vendors/<int:vendor_id>", vendor_views.VendorViewAPI.as_view(), name="vendors.vendor-details"),
    path("api/<int:version>/vendors/<int:vendor_id>/performance", vendor_views.VendorPerformanceAPI.as_view(), name="vendors.vendor-performance"),
]
