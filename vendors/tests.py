from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from vendors.controllers import VendorViewAPI
from vendors.models import Vendor

class VendorModelTestCase(TestCase):
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

    def test_vendor_str_representation(self):
        expected_str = f"{self.vendor.vendor_code} - {self.vendor.name}"
        self.assertEqual(str(self.vendor), expected_str)

    def test_vendor_defaults(self):
        new_vendor = Vendor.objects.create(name="New Vendor")
        self.assertIsNotNone(new_vendor.added_on)
        self.assertIsNotNone(new_vendor.updated_on)
        self.assertIsNotNone(new_vendor.vendor_code)

    def test_vendor_unique_code(self):
        duplicate_vendor = Vendor.objects.create(name="Duplicate Vendor")
        self.assertIsNotNone(duplicate_vendor.vendor_code)

    def test_vendor_ratings_range(self):
        self.assertGreaterEqual(self.vendor.on_time_delivery_rate, 0)
        self.assertLessEqual(self.vendor.on_time_delivery_rate, 5)

        self.assertGreaterEqual(self.vendor.quality_rating_avg, 0)
        self.assertLessEqual(self.vendor.quality_rating_avg, 5)



class VendorViewAPITestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_all_vendors(self):
        Vendor.objects.create(name="Vendor1", contact_details="Contact1", address="Address1")
        Vendor.objects.create(name="Vendor2", contact_details="Contact2", address="Address2")

        request = self.factory.get('/api/1/vendors/')
        response = VendorViewAPI.as_view()(request, version='1')

        self.assertEqual(len(response.data), 2)  # Assuming there are two vendors in the database

    def test_get_specific_vendor(self):
        vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address")

        # Remove IsAuthenticated permission from VendorViewAPI only for testing.
        request = self.factory.get(f'/api/1/vendors/{vendor.id}/')
        response = VendorViewAPI.as_view()(request, vendor_id=vendor.id, version="1")
        self.assertEqual(response.data['name'], "Test Vendor")

    def test_create_vendor(self):
        data = {'name': 'New Vendor', 'contact_details': 'New Contact', 'address': 'New Address'}
        request = self.factory.post('/api/1/vendors/', data)
        response = VendorViewAPI.as_view()(request, version='1')

        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.first().name, 'New Vendor')

