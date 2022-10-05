from datetime import datetime
import email
import uuid
from django.db import models

from userprofiles.models import Profiles

# Create your models here.


class Product(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, 
        editable=False)
    vendor = models.ForeignKey(
        Profiles, related_name='product_vendor_profile',
        on_delete=models.CASCADE, blank=True,
        null=True)
    name = models.CharField(
        max_length=255, null=False)
    description = models.TextField(
        blank=True, null=True)
    price = models.DecimalField(
        max_digits=9, decimal_places=2)
    brand = models.CharField(
        max_length=255, blank = True, null=True)
    rating = models.IntegerField(
        null=True, blank=True)
    created_at = models.DateTimeField(
        blank = True)
    updated_at = models.DateTimeField(
        blank = True)
    is_deleted = models.BooleanField(
        default=False)


    def save(self, *args, **kwargs):

        current_time = datetime.now()

        if not self.created_at:
            self.created_at = current_time

        self.updated_at = current_time

        super(Product, self).save(*args, **kwargs)
    
        return self