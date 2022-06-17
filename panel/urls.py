from django.urls import path, include
from panel.views import DashboardView

app_name = "panel"

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),

    path("doctors/", include('doctor.urls'), name="doctor"),
    path("patients/", include('patient.urls'), name="patient"),
    path("reports/", include('report.urls'), name="report"),
    path("products/", include('product.urls'), name="product"),
    path("appointments/", include('appointment.urls'), name="appointment"),
    path("prescriptions/", include('prescription.urls'), name="prescription"),

]