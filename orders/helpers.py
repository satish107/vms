from datetime import datetime
from django.db.models import Q, F, Avg

def vendor_on_time_delivery_rate(vendor):
	from orders.models import PurchaseOrder
	rate = None
	vendor_completed_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, status=PurchaseOrder.COMPLETED)
	on_time_deleveries = vendor_completed_purchase_orders.filter(actual_delivery_date__lte=F('expected_delivery_date'))
	if on_time_deleveries.count() > 0:
		rate = on_time_deleveries.count()/vendor_completed_purchase_orders.count()
	return round(rate, 2)

def vendor_avg_quality_rating(vendor):
	from orders.models import PurchaseOrder
	return PurchaseOrder.objects.filter(vendor=vendor, status=PurchaseOrder.COMPLETED).aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']

def vendor_average_response_time(vendor):
	from orders.models import PurchaseOrder
	average_response_time = None
	average_time_response = PurchaseOrder.objects.filter(vendor=vendor).annotate(response_time=F("acknowledgement_date") - F("issue_date")).aggregate(average_time_response=Avg("response_time"))["average_time_response"]
	if average_time_response:
		average_response_time = round(average_time_response.total_seconds(), 2)
	return average_response_time

def vendor_fulfilment_rate(vendor):
	from orders.models import PurchaseOrder
	fulfilment_rate = None
	completed_pos = PurchaseOrder.objects.filter(vendor=vendor.id, status=PurchaseOrder.COMPLETED)
	pos_issued = PurchaseOrder.objects.filter(vendor=vendor, issue_date__isnull=True)
	if pos_issued.count() > 0:
		fulfilment_rate = round(completed_pos.count()/pos_issued.count(), 2)
	return fulfilment_rate