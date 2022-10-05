from datetime import datetime
import email
import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profiles(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, 
        editable=False)
    user = models.ForeignKey(
        User, related_name='profiles_user',
        on_delete=models.CASCADE, blank=True,
        null=True)
    name = models.CharField(
        max_length=255, null=False)
    email = models.CharField(
        unique=True, blank=True, 
        max_length=255, null=True)
    profile_type = models.CharField(
        max_length=255, blank=True, 
        null=True)
    dob = models.DateField(
        blank = True, null=True)
    gender = models.CharField(
        max_length=10, null=True, 
        blank=True)
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

        super(Profiles, self).save(*args, **kwargs)
    
        return self