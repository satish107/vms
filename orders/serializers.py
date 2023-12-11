from rest_framework import serializers
from orders.models import PurchaseOrder, HistoricalPerformance

class PurchaseOrderSerializer(serializers.ModelSerializer):

	class Meta:
		model = PurchaseOrder
		fields = (
				'id', 'po_number', 'vendor', 'order_date', 'expected_delivery_date',
				'actual_delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date',
				'acknowledgement_date'
			)


class HistoricalPerformanceSerializer(serializers.ModelSerializer):

	class Meta:
		model = HistoricalPerformance
		fields = (
				'id', 'vendor', 'date', 'on_time_delevery_rate', 'quality_rating_avg',
				'average_response_time', 'fulfilment_rate'
			)