from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowRecord
@receiver(post_save, sender=BorrowRecord)
def update_equipment_status(sender, instance, created, **kwargs):
    equipment = instance.equipment
    if not instance.is_returned:
        equipment.status = 'borrowed'
    else:
        equipment.status = 'available'
    equipment.save()