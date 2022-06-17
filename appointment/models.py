from django.db import models
from accounts.models import User


class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="appointment_doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="appointment_patient")
    appointmentDate = models.DateTimeField(blank=False, null=False)
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
