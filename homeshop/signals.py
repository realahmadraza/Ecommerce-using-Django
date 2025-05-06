from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Sales

@receiver(post_save, sender=Order)
def update_sales(sender, instance, **kwargs):
    sales_entry, created = Sales.objects.get_or_create(product=instance.product)
    sales_entry.sales += instance.quantity
    sales_entry.save()