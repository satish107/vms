from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from vendors.models import Vendor
from vendors import serializers
from orders.models import HistoricalPerformance
from orders import serializers as order_serializers

from rest_framework.permissions import IsAuthenticated

class VendorViewAPI(APIView):

	"""
	    API endpoint for interacting with vendors.
		- End Point: api/version/vendors
	    - GET: List all vendors or retrieve a specific vendor.
	    - POST: Create a new vendor.
	    - PUT: Update a specific vendor.
	    - DELETE: Delete a specific vendor or all vendors.
    """

	permission_classes = (IsAuthenticated,)

	def get(self, request, version, vendor_id=None):
		if vendor_id is not None:
			vendor = get_object_or_404(Vendor, id=vendor_id)
			serializer = serializers.VendorSerializer(vendor)
		else:
			vendors = Vendor.objects.all()
			serializer = serializers.VendorSerializer(vendors, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, version):
		serializer = serializers.VendorSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, version, vendor_id=None):
		if vendor_id is not None:
			vendor = get_object_or_404(Vendor, id=vendor_id)
			serializer = serializers.VendorSerializer(vendor, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'message': 'Please Provide Valid vendor_id'}, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, version, vendor_id=None):
		if vendor_id is not None:
			vendor = Vendor.objects.get(id=vendor_id)
			vendor.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			vendors = Vendor.objects.all()
			vendors.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)


class VendorPerformanceAPI(APIView):

	"""
	    API endpoint for vendor performance.
		- End Point: api/version/vendors/<int:vendor_id>/performance
	    - GET: Retrieve a specific vendor.
    """

	permission_classes = (IsAuthenticated,)

	def get(self, request, version, vendor_id):
		if vendor_id is not None:
			vendor = get_object_or_404(Vendor, id=vendor_id)
			historical_performance = HistoricalPerformance.objects.filter(vendor=vendor).last()
			serializer = order_serializers.HistoricalPerformanceSerializer(historical_performance)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response({"message": "Enter Valid Vendor Id."}, status=status.HTTP_400_BAD_REQUEST)
