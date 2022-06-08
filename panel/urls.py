from django.urls import path

from .views import DashboardView, PrescriptionsView, DoctorsView, ReportsView, PatientsView, LoginView, RegisterView, \
    IndexView, LogoutView, DoctorView, PatientView, PrescriptionView, ReportView, AddDoctorView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("panel/", DashboardView.as_view(), name="panel"),
    path("panel/dashboard", DashboardView.as_view(), name="dashboard"),
    path("panel/prescriptions", PrescriptionsView.as_view(), name="prescriptions"),
    path("panel/doctors/<int:pk>", DoctorView.as_view(), name="doctor"),
    path("panel/doctors/new", AddDoctorView.as_view(), name="add_doctor"),
    path("panel/patients/<int:pk>", PatientView.as_view(), name="patient"),
    path("panel/patients/new", AddDoctorView.as_view(), name="add_patient"),
    path("panel/prescriptions/<int:pk>", PrescriptionView.as_view(), name="prescription"),
    path("panel/prescriptions/new", AddDoctorView.as_view(), name="add_prescription"),
    path("panel/reports/<int:pk>", ReportView.as_view(), name="report"),
    path("panel/reports/new", ReportView.as_view(), name="add_report"),
    path("panel/doctors", DoctorsView.as_view(), name="doctors"),
    path("panel/reports", ReportsView.as_view(), name="reports"),
    path("panel/patients", PatientsView.as_view(), name="patients"),
]