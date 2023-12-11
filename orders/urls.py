from django.urls import path, include
from django.contrib import admin

from orders import controllers as purchase_orders_views

urlpatterns = [
    path("api/<int:version>/purchase_orders/", purchase_orders_views.PurchaseOrderView.as_view(), name="orders.purchase-orders-list"),
    path("api/<int:version>/purchase_orders/<int:po_id>", purchase_orders_views.PurchaseOrderView.as_view(), name="orders.purchase-orders-details"),
    path("api/<int:version>/purchase_orders/<int:po_id>/acknowledge", purchase_orders_views.AcknowledgePurchaseOrder.as_view(), name="orders.purchase-orders-acknoledge"),
]
