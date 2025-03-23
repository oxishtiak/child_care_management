from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    mobile = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    phone = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user.username    

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(default=0)
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to='child_images/')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} ({self.unique_id})"
    

class Package(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()  
    description = models.TextField()
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.duration_days} days) - BDT {self.price}"
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    parent = models.ForeignKey('Parent', on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings')
    children = models.ManyToManyField('Child', related_name='bookings')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField()  
    end_date = models.DateField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Automatically calculate total price and end date before saving. """
        if not self.end_date:
            from datetime import timedelta
            self.end_date = self.start_date + timedelta(days=self.package.duration_days)

        if not self.total_price:
            self.total_price = self.package.price  

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.user.username} - {self.package.name} - {self.status}"

class Transaction(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Credit/Debit Card'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('cash', 'Cash on Delivery'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='transaction')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_successful = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.booking.parent.user.username}" 


