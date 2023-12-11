import uuid
from datetime import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.core.exceptions import ValidationError
from vendors.models import Vendor
from orders.helpers import vendor_on_time_delivery_rate, vendor_avg_quality_rating, vendor_average_response_time, vendor_fulfilment_rate
from vendors.helpers import generate_unique_code

# Create your models here.

class PurchaseOrder(models.Model):

	PENDING = 1
	CANCELLED = 2
	COMPLETED = 3

	ORDER_STATUS = (
			(PENDING, 'Pending'),
			(CANCELLED, 'Cancelled'),
			(COMPLETED, 'Completed')
		)

	po_number = models.CharField(max_length=255, null=True, blank=True, unique=True, default=generate_unique_code, editable=False)
	vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
	order_date = models.DateTimeField(auto_now_add=True)
	expected_delivery_date = models.DateTimeField(null=True)
	actual_delivery_date = models.DateTimeField(null=True)
	items = models.JSONField(null=True, blank=True)
	quantity = models.PositiveSmallIntegerField(null=True, blank=True)
	status = models.PositiveSmallIntegerField(choices=ORDER_STATUS, default=PENDING)
	quality_rating = models.FloatField(null=True, blank=True)
	issue_date = models.DateTimeField(null=True)
	acknowledgement_date = models.DateTimeField(null=True)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "purchase_order"
		verbose_name_plural = "purchase_order"

	def __str__(self):
		return f"{self.po_number} - {self.vendor.name}"

	def clean(self):
		if self.status not in dict(self.ORDER_STATUS).keys():
			raise ValidationError({'status': 'Invalid status value'})

	def save(self, *args, **kwargs):
		if not self.actual_delivery_date and self.status == PurchaseOrder.PENDING:
			self.actual_delivery_date = self.expected_delivery_date
		super(PurchaseOrder, self).save(*args, **kwargs)


def is_status_changed(instance):
	if instance.id is not None:
		original_instance = PurchaseOrder.objects.get(id=instance.id)
		return instance.status != original_instance.status
	return False

@receiver(pre_save, sender=PurchaseOrder)
def pre_save_handler(sender, instance=None, created=False, **kwargs):
	if is_status_changed(instance):
		vendor = instance.vendor
		vendor.fulfilment_rate = vendor_fulfilment_rate(vendor)
		vendor.save(update_fields=["fulfilment_rate"])
	else:
		pass

@receiver(post_save, sender=PurchaseOrder)
def post_save_handler(sender, instance=None, created=False, **kwargs):
	vendor = instance.vendor
	if not created:
		if instance.status == PurchaseOrder.COMPLETED:
			vendor.on_time_delivery_rate = vendor_on_time_delivery_rate(vendor)
			if instance.quality_rating:
				vendor.quality_rating_avg = vendor_avg_quality_rating(vendor)
			vendor.save(update_fields=["on_time_delivery_rate", "quality_rating_avg"])
		else:
			pass
	if not HistoricalPerformance.objects.filter(vendor_id=vendor.id).exists():
		HistoricalPerformance.objects.create(
				vendor=vendor,
				date=datetime.now(),
				on_time_delivery_rate=vendor.on_time_delivery_rate,
				quality_rating_avg=vendor.quality_rating_avg,
				average_response_time=vendor.average_response_time,
				fulfilment_rate=vendor.fulfilment_rate,
			)
	else:
		historical_performance = HistoricalPerformance.objects.filter(vendor_id=vendor.id).last()
		historical_performance.date = datetime.now()
		historical_performance.on_time_delivery_rate = vendor.on_time_delivery_rate
		historical_performance.quality_rating_avg = vendor.quality_rating_avg
		historical_performance.average_response_time = vendor.average_response_time
		historical_performance.fulfilment_rate = vendor.fulfilment_rate
		historical_performance.save()



class HistoricalPerformance(models.Model):
	vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	on_time_delivery_rate = models.FloatField(null=True, blank=True)
	quality_rating_avg = models.FloatField(null=True, blank=True)
	average_response_time = models.FloatField(null=True, blank=True)
	fulfilment_rate = models.FloatField(null=True, blank=True)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "historical_performance"
		verbose_name_plural = "historical_performances"

	def __str__(self):
		return f"{self.vendor.name} - {self.quality_rating_avg}"
