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
    order_number = models.CharField(max_length=20, unique = True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

