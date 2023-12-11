from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import PurchaseOrder
from orders import serializers
from orders.helpers import vendor_average_response_time


class PurchaseOrderView(APIView):

	"""
	    API endpoint for interacting with Purchase Orders.
		- End Point: api/version/purchase_orders
	    - GET: List all orders or retrieve a specific order.
	    - POST: Create a new order.
	    - PUT: Update a specific order.
	    - DELETE: Delete a specific order or all orders.
    """

	permission_classes = (IsAuthenticated,)

	def get(self, request, version, po_id=None):
		try:
			if po_id is not None:
				purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
				purchase_order_serializer = serializers.PurchaseOrderSerializer(purchase_order)
			else:
				purchase_orders = PurchaseOrder.objects.all()
				purchase_order_serializer = serializers.PurchaseOrderSerializer(purchase_orders, many=True)
			return Response(purchase_order_serializer.data, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def post(self, request, version):
		try:
			purchase_order_serializer = serializers.PurchaseOrderSerializer(data=request.data)
			if purchase_order_serializer.is_valid():
				purchase_order_serializer.save()
				return Response(purchase_order_serializer.data, status=status.HTTP_201_CREATED)
			return Response(purchase_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def put(self, request, version, po_id=None):
		try:
			if po_id is not None:
				purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
				purchase_order_serializer = serializers.PurchaseOrderSerializer(purchase_order, data=request.data)
				if purchase_order_serializer.is_valid():
					purchase_order_serializer.save()
					return Response(purchase_order_serializer.data, status=status.HTTP_200_OK)
				return Response(purchase_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'message': 'Please Provide Valid po_id'}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def delete(self, request, version, po_id=None):
		try:
			if po_id is not None:
				purchase_order = PurchaseOrder.objects.get(id=po_id)
				purchase_order.delete()
				return Response(status=status.HTTP_204_NO_CONTENT)
			else:
				purchase_orders = PurchaseOrder.objects.all()
				purchase_orders.delete()
				return Response(status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AcknowledgePurchaseOrder(APIView):

	permission_classes = (IsAuthenticated,)

	def post(self, request, version, po_id):
		purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
		purchase_order.acknowledgement_date = datetime.now()
		purchase_order.save(update_fields=["acknowledgement_date"])
		vendor = purchase_order.vendor
		if vendor:
			vendor.average_response_time = vendor_average_response_time(vendor)
			vendor.save(update_fields=["average_response_time"])
			return Response({"message": f"Purchase Order {purchase_order.po_number} has been acknowledged by vendor."}, status=status.HTTP_200_OK)
		else:
			return Response({"message": "This Purchase Order is assigned to any vendor."}, status=status.HTTP_400_BAD_REQUEST)
