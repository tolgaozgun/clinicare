from django.urls import path, include
from .views import PatientsView, AddPatientView, PatientView, EditPatientView, DeletePatientView

app_name = "patient"

urlpatterns = [
    path("", PatientsView.as_view(), name="patients"),
    path("new", AddPatientView.as_view(), name="add_patient"),
    path("<int:pk>", PatientView.as_view(), name="patient"),
    path("<int:pk>/edit", EditPatientView.as_view(), name="edit_patient"),
    path("<int:pk>/delete", DeletePatientView.as_view(), name="delete_patient"),

]