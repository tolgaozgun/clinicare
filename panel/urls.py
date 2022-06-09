from django.urls import path

from .views import DashboardView, PrescriptionsView, DoctorsView, ReportsView, PatientsView, \
    DoctorView, PatientView, PrescriptionView, ReportView, AddDoctorView, AddPatientView, \
    AddPrescriptionView, AddReportView

urlpatterns = [
    path("", DashboardView.as_view(), name="panel"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("prescriptions", PrescriptionsView.as_view(), name="prescriptions"),
    path("doctors/<int:pk>", DoctorView.as_view(), name="doctor"),
    path("doctors/new", AddDoctorView.as_view(), name="add_doctor"),
    path("patients/<int:pk>", PatientView.as_view(), name="patient"),
    path("patients/new", AddPatientView.as_view(), name="add_patient"),
    path("prescriptions/<int:pk>", PrescriptionView.as_view(), name="prescription"),
    path("prescriptions/new", AddPrescriptionView.as_view(), name="add_prescription"),
    path("reports/<int:pk>", ReportView.as_view(), name="report"),
    path("reports/new", AddReportView.as_view(), name="add_report"),
    path("doctors", DoctorsView.as_view(), name="doctors"),
    path("reports", ReportsView.as_view(), name="reports"),
    path("patients", PatientsView.as_view(), name="patients"),
]