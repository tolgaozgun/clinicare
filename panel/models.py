from django.db import models
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    role = models.SmallIntegerField(editable=False, default=1)
    department = models.TextField(null=True, blank=True)  # For doctors
    status = models.fields.SmallIntegerField(editable=False, default=1)
    password = models.CharField(max_length=200)
    isActivated = models.BooleanField(editable=False, default=False)
    is2FAEnabled = models.BooleanField(editable=False, default=False)
    lastLogin = models.DateTimeField(editable=False, default=None, null=True)
    photo = models.ImageField(upload_to="profile", null=True, default="profile/avatar.png")
    # sessions =
    # ipAddresses =
    lastUpdated = models.DateTimeField(auto_now=True, editable=False)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=False)

    REQUIRED_FIELDS = ['name', 'surname', 'email']

    def __str__(self):
        if self is None:
            return "None"
        else:
            return self.name + " " + self.surname


class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="prescription_doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="prescription_patient")
    drugs = models.TextField(blank=False, null=False)
    files = models.FileField(upload_to="attachments/prescriptions", null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)


class Report(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="report_doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="report_patient")
    files = models.FileField(upload_to='attachments/reports')
    type = models.TextField(blank=False, null=False)
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)


# TODO: Generalize the treatments to more than one doctor


