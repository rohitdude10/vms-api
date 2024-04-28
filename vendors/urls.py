from django.urls import path
from vendors.views import CreateUserAPIView,VendorList, VendorDetail,PurchaseOrderListCreateAPIView , PurchaseOrderRetrieveUpdateDestroyAPIView,VendorPerformanceView,AcknowledgePurchaseOrder

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view(), name='create-user'),
    path('vendors/', VendorList.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/', VendorDetail.as_view(), name='vendor-detail'),
    # Purchase order management URLs
    path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<str:po_id>/acknowledge/', AcknowledgePurchaseOrder.as_view(), name='acknowledge_purchase_order'),
]
