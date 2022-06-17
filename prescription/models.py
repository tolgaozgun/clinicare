from django.db import models
from accounts.models import User


class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="prescription_doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="prescription_patient")
    drugs = models.TextField(blank=False, null=False)
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)


class PrescriptionFile(models.Model):
    file = models.FileField(upload_to="attachments/prescriptions", null=True, blank=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE,
                                     related_name="prescription_file_prescription")