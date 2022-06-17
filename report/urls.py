from django.urls import path
from .views import AddReportView, ReportView, EditReportView, ReportsView, DeleteReportView

app_name = "report"

urlpatterns = [
    path("", ReportsView.as_view(), name="reports"),
    path("new", AddReportView.as_view(), name="add_report"),
    path("<int:pk>", ReportView.as_view(), name="report"),
    path("<int:pk>/edit", EditReportView.as_view(), name="edit_report"),
    path("<int:pk>/delete", DeleteReportView.as_view(), name="delete_report"),

]