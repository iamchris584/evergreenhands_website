from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
import uuid



# Create your models here.
class Donation(models.Model):
    choice = [
        ('P', 'Pending'),
        ('F', 'Failed'),
        ('S', 'Successful')
    ]
    full_name = models.CharField(max_length=50)
    email = models.EmailField(null=False)
    amount = models.IntegerField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sumup_checkout_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(choices=choice, default='P')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class ContactForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=False)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


# content management section models

class Projects(models.Model):
    choice = [
            ('UPCOMING', 'UPCOMING'),
            ('ACTIVE', 'ACTIVE'),
        ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    status = models.CharField(choices=choice, default='UPCOMING')
    order = models.PositiveIntegerField(default=0, help_text="Control display order on the homepage")
    date_label = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="e.g., CHRISTMAS 2026, EASTER 2027, ADVOCACY"
    )
    scheduled_date = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="e.g., CHRISTMAS 2026, EASTER 2027, ADVOCACY")
    read_time = models.CharField(
        max_length=50, 
        default="5 mins read", 
        help_text="e.g., 5 mins read, Holiday Relief, Patient Voice"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

class TeamMemeber(models.Model):
    full_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='team/' , blank=True, null=True)
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name

