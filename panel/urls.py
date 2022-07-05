from django.urls import path, include
from panel.views import *

app_name = "panel"

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),

    # Messaging URLs
    path("messaging", MessagingView.as_view(), name="messaging"),

    # Doctor URLs
    path("doctors/", DoctorsView.as_view(), name="doctors"),
    path("doctors/new", AddDoctorView.as_view(), name="add_doctor"),
    path("doctors/<int:pk>", DoctorView.as_view(), name="doctor"),
    path("doctors/<int:pk>/edit", EditDoctorView.as_view(), name="edit_doctor"),
    path("doctors/<int:pk>/delete", EditDoctorView.as_view(), name="delete_doctor"),

    # Patient URLs
    path("patients/", PatientsView.as_view(), name="patients"),
    path("patients/new", AddPatientView.as_view(), name="add_patient"),
    path("patients/<int:pk>", PatientView.as_view(), name="patient"),
    path("patients/<int:pk>/edit", EditPatientView.as_view(), name="edit_patient"),
    path("patients/<int:pk>/delete", DeletePatientView.as_view(), name="delete_patient"),

    # Product URLs
    path("products/", ProductsView.as_view(), name="products"),
    path("products/new", AddProductView.as_view(), name="add_product"),
    path("products/<int:pk>", ProductView.as_view(), name="product"),
    path("products/<int:pk>/edit", EditProductView.as_view(), name="edit_product"),
    path("products/<int:pk>/delete", DeleteProductView.as_view(), name="delete_product"),

    # Report URLs
    path("reports/", ReportsView.as_view(), name="reports"),
    path("reports/new", AddReportView.as_view(), name="add_report"),
    path("reports/<int:pk>", ReportView.as_view(), name="report"),
    path("reports/<int:pk>/edit", EditReportView.as_view(), name="edit_report"),
    path("reports/<int:pk>/delete", DeleteReportView.as_view(), name="delete_report"),

    # Appointment URLs
    path("appointments/", AppointmentsView.as_view(), name="appointments"),
    path("appointments/new", AddAppointmentView.as_view(), name="add_appointment"),
    path("appointments/<int:pk>/new", DoctorAddAppointmentView.as_view(), name="dr_add_appointment"),
    path("appointments/<int:pk>", AppointmentView.as_view(), name="appointment"),
    path("appointments/<int:pk>/edit", AppointmentView.as_view(), name="edit_appointment"),
    path("appointments/<int:pk>/delete", AppointmentView.as_view(), name="delete_appointment"),

    # Prescription URLs
    path("prescriptions/", PrescriptionsView.as_view(), name="prescriptions"),
    path("prescriptions/new", AddPrescriptionView.as_view(), name="add_prescription"),
    path("prescriptions/<int:pk>", PrescriptionView.as_view(), name="prescription"),
    path("prescriptions/int:pk>/edit", EditPrescriptionView.as_view(), name="edit_prescription"),
    path("prescriptions/<int:pk>/delete", DeletePrescriptionView.as_view(), name="delete_prescription"),

]