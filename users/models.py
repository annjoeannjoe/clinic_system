from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class Property(models.Model):
    property_name = models.CharField(max_length=100)

    def __str__(self):
        return self.property_name
    
class Patient(models.Model):
    fullname = models.CharField(max_length=100)
    nric_passport = models.CharField(max_length=20, unique=True)
    dob = models.DateField()
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    allergies = models.ManyToManyField(Property, related_name='patients_with_allergy')
    def soft_delete(self):
        self.deleted = True
        self.save()
    
class Medication(models.Model):
    medication_name = models.CharField(max_length=100)
    properties = models.ManyToManyField(Property)

    def __str__(self):
        return self.medication_name
    
class MedicationOrder(models.Model):
    STATUS_CHOICES =(
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
    )
    order_number = models.CharField(max_length=20, blank=True, null=True)
    order_status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default='Pending')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medications = models.ManyToManyField(Medication, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(MedicationOrder, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()