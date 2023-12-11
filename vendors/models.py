from django.db import models
from django.core.exceptions import ValidationError
from vendors.helpers import generate_unique_code

# Create your models here.

class Vendor(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True)
	contact_details = models.TextField(null=True, blank=True)
	address = models.TextField(null=True, blank=True)
	vendor_code = models.CharField(max_length=255, null=True, blank=True, unique=True, default=generate_unique_code)
	on_time_delevery_rate = models.FloatField(null=True, blank=True)
	quality_rating_avg = models.FloatField(null=True, blank=True)
	average_response_time = models.FloatField(null=True, blank=True)
	fulfilment_rate = models.FloatField(null=True, blank=True)
	added_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "vendor"
		verbose_name_plural = "vendors"

	def __str__(self):
		return f"{self.vendor_code} - {self.name}"
