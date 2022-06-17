from django.urls import path
from .views import PrescriptionsView, AddPrescriptionView, PrescriptionView, EditPrescriptionView, \
    DeletePrescriptionView

app_name = "prescription"

urlpatterns = [

    path("", PrescriptionsView.as_view(), name="prescriptions"),
    path("new", AddPrescriptionView.as_view(), name="add_prescription"),
    path("<int:pk>", PrescriptionView.as_view(), name="prescription"),
    path("<int:pk>/edit", EditPrescriptionView.as_view(), name="edit_prescription"),
    path("<int:pk>/delete", DeletePrescriptionView.as_view(), name="delete_prescription"),
]