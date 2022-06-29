from django.urls import path
from .views import AppointmentsView, AddAppointmentView, AppointmentView, DoctorAddAppointmentView

app_name = "appointment"

urlpatterns = [

    path("", AppointmentsView.as_view(), name="appointments"),
    path("new", AddAppointmentView.as_view(), name="add_appointment"),
    path("<int:pk>/new", DoctorAddAppointmentView.as_view(), name="dr_add_appointment"),
    path("<int:pk>", AppointmentView.as_view(), name="appointment"),
    path("<int:pk>/edit", AppointmentView.as_view(), name="edit_appointment"),
    path("<int:pk>/delete", AppointmentView.as_view(), name="delete_appointment"),
]