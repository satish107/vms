from django.test import TestCase
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.exceptions import ValidationError
from vendors.models import Vendor
from orders.models import PurchaseOrder

class PurchaseOrderModelTestCase(TestCase):
    def setUp(self):

        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
            on_time_delivery_rate=4.5,
            quality_rating_avg=3.8,
            average_response_time=2.5,
            fulfilment_rate=95.0,
        )

        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            expected_delivery_date="2023-12-31T12:00:00Z",
            items={'item1': 2, 'item2': 5},
            quantity=7,
            status=PurchaseOrder.PENDING,
            quality_rating=4.2,
        )

    def test_purchase_order_defaults(self):
        new_purchase_order = PurchaseOrder.objects.create(vendor=self.vendor)
        self.assertIsNotNone(new_purchase_order.po_number)
        self.assertIsNotNone(new_purchase_order.order_date)
        self.assertIsNone(new_purchase_order.actual_delivery_date)
        self.assertIsNone(new_purchase_order.issue_date)
        self.assertIsNone(new_purchase_order.acknowledgement_date)

    def test_purchase_order_unique_po_number(self):
        duplicate_purchase_order = PurchaseOrder.objects.create(vendor=self.vendor)
        self.assertIsNotNone(duplicate_purchase_order.po_number)

    def test_purchase_order_status_choices(self):
        with self.assertRaises(ValidationError):
        	invalid_status_order = PurchaseOrder.objects.create(vendor=self.vendor, status=99)
        	self.assertEqual(invalid_status_order.status, PurchaseOrder.PENDING)

    def test_purchase_order_ratings_range(self):
        self.assertGreaterEqual(self.purchase_order.quality_rating, 0)
        self.assertLessEqual(self.purchase_order.quality_rating, 5)


class PurchaseOrderViewTestCase(TestCase):

	def setUp(self):
		self.client = APIClient()

	def test_get_all_orders(self):
		# Create some sample purchase orders
		vendor1 = Vendor.objects.create(name="Test Vendor 1", contact_details="contact_details", address="address")
		vendor2 = Vendor.objects.create(name="Test Vendor 2", contact_details="contact_details", address="address")
		PurchaseOrder.objects.create(vendor=vendor1, quantity=10, status=PurchaseOrder.PENDING)
		PurchaseOrder.objects.create(vendor=vendor2, quantity=5, status=PurchaseOrder.COMPLETED)

		# Make a GET request to retrieve all orders
		response = self.client.get('/api/1/purchase_orders/')

		self.assertEqual(len(response.data), 2)  # Assuming there are two purchase orders in the database

	def test_get_specific_order(self):
		# Create a sample purchase order
		vendor = Vendor.objects.create(name="Test Vendor", contact_details="contact_details", address="address")
		purchase_order = PurchaseOrder.objects.create(vendor=vendor, quantity=8, status=PurchaseOrder.PENDING)

		# Make a GET request to retrieve the specific order
		response = self.client.get(f'/api/1/purchase_orders/{purchase_order.id}/')
		self.assertEqual(response.data['vendor'], vendor)

	def test_create_order(self):
		# Need to remove isAuthenticated permission in order to create Purchase Order
		vendor = Vendor.objects.create(name="Test Vendor", contact_details="contact_details", address="address")
		data = {'vendor': vendor.id, 'quantity': 12, 'status': PurchaseOrder.PENDING}
		response = self.client.post('/api/1/purchase_orders/', data)
		self.assertEqual(response.data['vendor'], vendor.id)


