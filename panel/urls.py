from django.urls import path

from .views import DashboardView, PrescriptionsView, DoctorsView, ReportsView, PatientsView, \
    DoctorView, PatientView, PrescriptionView, ReportView, AddDoctorView, AddPatientView, \
    AddPrescriptionView, AddReportView, EditPatientView, EditDoctorView, EditPrescriptionView, EditReportView, ProductView, ProductsView

urlpatterns = [
    path("", DashboardView.as_view(), name="panel"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),

    path("doctors", DoctorsView.as_view(), name="doctors"),
    path("doctors/new", AddDoctorView.as_view(), name="add_doctor"),
    path("doctors/<int:pk>", DoctorView.as_view(), name="doctor"),
    path("doctors/<int:pk>/edit", EditDoctorView.as_view(), name="edit_doctor"),
    path("doctors/<int:pk>/delete", EditDoctorView.as_view(), name="delete_doctor"),

    path("patients", PatientsView.as_view(), name="patients"),
    path("patients/new", AddPatientView.as_view(), name="add_patient"),
    path("patients/<int:pk>", PatientView.as_view(), name="patient"),
    path("patients/<int:pk>/edit", EditPatientView.as_view(), name="edit_patient"),
    path("patients/<int:pk>/delete", EditPatientView.as_view(), name="delete_patient"),

    path("prescriptions", PrescriptionsView.as_view(), name="prescriptions"),
    path("prescriptions/new", AddPrescriptionView.as_view(), name="add_prescription"),
    path("prescriptions/<int:pk>", PrescriptionView.as_view(), name="prescription"),
    path("prescriptions/<int:pk>/edit", EditPrescriptionView.as_view(), name="edit_prescription"),
    path("prescriptions/<int:pk>/delete", EditPrescriptionView.as_view(), name="delete_prescription"),

    path("reports", ReportsView.as_view(), name="reports"),
    path("reports/new", AddReportView.as_view(), name="add_report"),
    path("reports/<int:pk>", ReportView.as_view(), name="report"),
    path("reports/<int:pk>/edit", EditReportView.as_view(), name="edit_report"),
    path("reports/<int:pk>/delete", EditReportView.as_view(), name="delete_report"),

    path("products", ProductsView.as_view(), name="products"),
    path("products/new", ProductsView.as_view(), name="add_product"),
    path("products/<int:pk>", ProductView.as_view(), name="product"),
    path("products/<int:pk>/edit", ProductView.as_view(), name="edit_product"),
    path("products/<int:pk>/delete", ProductView.as_view(), name="delete_product"),

    path("appointments", ProductsView.as_view(), name="appointments"),
    path("appointments/new", ProductsView.as_view(), name="add_appointment"),
    path("appointments/<int:pk>", ProductView.as_view(), name="appointment"),
    path("appointments/<int:pk>/edit", ProductView.as_view(), name="edit_appointment"),
    path("appointments/<int:pk>/delete", ProductView.as_view(), name="delete_appointment"),
]