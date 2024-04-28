# myapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor, HistoricalPerformance
from django.utils import timezone
from django.db.models import Avg, F, ExpressionWrapper, F,DurationField, Count

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_orders = completed_orders.count()
        on_time_delivered_orders = completed_orders.filter(actual_delivery_date__lte=instance.expected_delivery_date).count()
        on_time_delivery_rate = (on_time_delivered_orders / total_completed_orders) * 100 if total_completed_orders else 0
        print("runing signnals============>")
        print("completed orders", completed_orders)
        print("total_completed_orders", total_completed_orders)
        print("on_time_delivered_orders", on_time_delivered_orders)
        print("on_time_delivery_rate", on_time_delivery_rate)
        # Create or update Historical Performance
        historical_performance, _ = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=timezone.now())
        historical_performance.on_time_delivery_rate = on_time_delivery_rate
        historical_performance.save()


@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        quality_rating_avg = completed_orders.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

        # Create or update Historical Performance
        historical_performance, _ = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=timezone.now())
        historical_performance.quality_rating_avg = quality_rating_avg
        historical_performance.save()
        
        
        
@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if not created and instance.acknowledgment_date:
        print("acknowledgment_date")
        vendor = instance.vendor
        ack_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = ack_orders.annotate(response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField()))
        avg_response_time = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
        
        # Convert timedelta object to total seconds
        avg_response_time_seconds = avg_response_time.total_seconds() if avg_response_time else 0
        # Create or update Historical Performance
        historical_performance, _ = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=timezone.now())
        historical_performance.average_response_time = avg_response_time_seconds
        historical_performance.save()
        
        
@receiver([post_save], sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    fulfilment_rate = (fulfilled_orders.count() / total_orders) if total_orders != 0 else 0

    # Create or update Historical Performance
    historical_performance, _ = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=timezone.now())
    historical_performance.fulfillment_rate = fulfilment_rate
    historical_performance.save()