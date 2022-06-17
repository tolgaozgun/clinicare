from django.db import models
from accounts.models import User


class Report(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="report_doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="report_patient")
    type = models.TextField(blank=False, null=False)
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)


class ReportFile(models.Model):
    file = models.FileField(upload_to='attachments/reports')
    report = models.ForeignKey(Report, on_delete=models.CASCADE,
                               related_name="report_file_report")