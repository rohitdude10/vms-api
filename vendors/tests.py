from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer

class VendorAPITests(APITestCase):
    def setUp(self):
        # Create sample vendors for testing
        self.vendor1 = Vendor.objects.create(
            name="Vendor 1",
            contact_details="Contact details for Vendor 1",
            address="Address of Vendor 1",
            vendor_code="VENDOR001"            
        )
        self.vendor2 = Vendor.objects.create(
            name="Vendor 2",
            contact_details="Contact details for Vendor 2",
            address="Address of Vendor 2",
            vendor_code="VENDOR002"            
        )

    def test_get_vendors(self):
        # Test retrieving all vendors
        url = reverse('vendor-list')  # URL to the vendor list endpoint
        response = self.client.get(url)  # Send a GET request to the endpoint
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the number of vendors returned matches the number created in setUp
        self.assertEqual(len(response.data), 2)

class PurchaseOrderAPITests(APITestCase):
    def setUp(self):
        # Create sample vendor for testing
        self.vendor = Vendor.objects.create(
            name="Vendor",
            contact_details="Contact details for Vendor",
            address="Address of Vendor",
            vendor_code="VENDOR001",
            on_time_delivery_rate=90.5,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=95.7
        )
        # Create sample purchase orders for testing
        self.purchase_order1 = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO001",
            order_date="2024-04-30",
            items={},
            quantity=10,
            status="completed",
            quality_rating=4.0,
            issue_date="2024-04-30T10:00:00Z",
            acknowledgment_date="2024-04-30T10:05:00Z",
            expected_delivery_date="2024-05-05T10:00:00Z",
            actual_delivery_date="2024-05-04T10:00:00Z"
        )
        self.purchase_order2 = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO002",
            order_date="2024-05-01",
            items={},
            quantity=8,
            status="pending",
            quality_rating=None,
            issue_date="2024-05-01T09:00:00Z",
            acknowledgment_date=None,
            expected_delivery_date="2024-05-10T09:00:00Z",
            actual_delivery_date=None
        )

    def test_get_purchase_orders(self):
        # Test retrieving all purchase orders
        url = reverse('purchase-order-list-create')  # URL to the purchase order list-create endpoint
        response = self.client.get(url)  # Send a GET request to the endpoint
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the number of purchase orders returned matches the number created in setUp
        self.assertEqual(len(response.data), 2)

    # Add more test cases for other methods in PurchaseOrderListCreateAPIView and PurchaseOrderRetrieveUpdateDestroyAPIView

class VendorPerformanceAPITests(APITestCase):
    def setUp(self):
        # Create sample vendor for testing
        self.vendor = Vendor.objects.create(
            name="Vendor",
            contact_details="Contact details for Vendor",
            address="Address of Vendor",
            vendor_code="VENDOR001",
            on_time_delivery_rate=90.5,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=95.7
        )
        # Create sample historical performance data for the vendor
        self.historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date="2024-04-30",
            on_time_delivery_rate=90.5,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=95.7
        )

    def test_get_vendor_performance(self):
        # Test retrieving vendor performance metrics
        url = reverse('vendor-performance', kwargs={'vendor_id': self.vendor.pk})
        response = self.client.get(url)
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add more test cases for other methods in VendorPerformanceView

class AcknowledgePurchaseOrderAPITests(APITestCase):
    def setUp(self):        
        self.vendor = Vendor.objects.create(
            name="Vendor",
            contact_details="Contact details for Vendor",
            address="Address of Vendor",
            vendor_code="VENDOR001",
            on_time_delivery_rate=90.5,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=95.7
        )
        # Create a sample purchase order for testing
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO003",
            vendor=self.vendor,
            order_date="2024-04-30",
            items={},
            quantity=10,
            status="pending",
            quality_rating=None,
            issue_date="2024-04-30T10:00:00Z",
            acknowledgment_date=None,
            expected_delivery_date="2024-05-05T10:00:00Z",
            actual_delivery_date=None
        )

    def test_acknowledge_purchase_order(self):
        # Test acknowledging a purchase order
        url = reverse('acknowledge_purchase_order', kwargs={'po_id': self.purchase_order.po_number})
        response = self.client.post(url)
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

   
