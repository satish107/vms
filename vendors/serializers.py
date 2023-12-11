from rest_framework import serializers
from vendors.models import Vendor

class VendorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Vendor
		fields = (
				'id', 'name', 'contact_details', 'address', 'vendor_code',
				'on_time_delevery_rate', 'quality_rating_avg', 'average_response_time', 'fulfilment_rate', 
				'added_on', 'updated_on'
			)
