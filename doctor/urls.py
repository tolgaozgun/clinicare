from django.urls import path
from .views import DoctorsView, AddDoctorView, DoctorView, EditDoctorView

app_name = "doctor"

urlpatterns = [
    path("", DoctorsView.as_view(), name="doctors"),
    path("new", AddDoctorView.as_view(), name="add_doctor"),
    path("<int:pk>", DoctorView.as_view(), name="doctor"),
    path("<int:pk>/edit", EditDoctorView.as_view(), name="edit_doctor"),
    path("<int:pk>/delete", EditDoctorView.as_view(), name="delete_doctor"),
]