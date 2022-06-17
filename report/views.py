from accounts.models import User
from clinic.settings import MODELS_PER_PAGE
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views import View
from panel.roles import Roles

from .forms import ReportForm
from .models import Report, ReportFile


class PanelView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect'


class ReportView(PanelView):
    def get(self, request, pk):
        is_valid = False
        try:
            report = Report.objects.get(id=pk)
            is_valid = True
        except Report.DoesNotExist:
            report = Report(doctor=None,
                            patient=None,
                            files=None,
                            dateCreated=None,
                            lastUpdated=None)
            is_valid = False  # Failsafe
        report.files = report.report_file_report.all()
        context = {'is_valid': is_valid, 'current_page': 'view_report', 'report': report}
        return render(request, 'report/report.html', context)


class ReportsView(PanelView):
    def get(self, request):
        reports = Report.objects.all()
        paginator = Paginator(reports, MODELS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'current_page': 'reports', 'reports': page_obj}
        return render(request, 'report/reports.html', context)


class AddReportView(PanelView):
    def get(self, request):
        form = ReportForm()
        form.fields['patient'].queryset = User.objects.filter(role=Roles.PATIENT.value)
        form.fields['doctor'].queryset = User.objects.filter(role=Roles.DOCTOR.value)
        context = {"current_page": "add_report", "form": form}
        return render(request, 'report/add_report.html', context)

    def post(self, request):
        form = ReportForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')

        if form.is_valid():
            form.cleaned_data.pop('files')
            form.cleaned_data.pop('captcha')
            new_report = Report(**form.cleaned_data,
                                dateCreated=now,
                                lastUpdated=now)
            new_report.save()
            for f in files:
                file = ReportFile(file=f, report=new_report)
                file.save()
            return redirect('panel:report:reports')
        else:
            context = {"current_page": "add_report", "form": form}
            return render(request, "report/add_report.html", context)


class EditReportView(PanelView):
    def get(self, request, pk):
        report = Report.objects.get(id=pk)
        form = ReportForm(instance=report)
        form.fields['patient'].queryset = User.objects.filter(role=Roles.PATIENT.value)
        form.fields['doctor'].queryset = User.objects.filter(role=Roles.DOCTOR.value)
        context = {'current_page': 'edit_report', 'form': form}
        return render(request, 'report/add_report.html', context)

    def post(self, request, pk):

        try:
            report = Report.objects.get(id=pk)
        except Report.DoesNotExist:
            context = {'current_page': 'edit_report', 'form': ReportForm()}
            messages.error(request, "Report not found")
            return render(request, "report/add_report.html", context)

        form = ReportForm(request.POST, request.FILES, instance=report)
        files = request.FILES.getlist('files')

        if form.is_valid():
            form.cleaned_data.pop('files')
            form.cleaned_data.pop('captcha')
            report.lastUpdated = now
            report.save()

            for f in files:
                file = ReportFile(file=f, report=report)
                file.save()
            return redirect('panel:report:reports')
        else:
            context = {'current_page': 'edit_report', 'form': form}
            return render(request, "report/add_report.html", context)


class DeleteReportView(PanelView):
    def get(self, request, pk):
        context = {'current_page': 'delete_report'}
        return render(request, 'report/delete_report.html', context)

    def post(self, request, pk):
        if 'answer_no' in request.POST:
            return redirect('panel:report:report', pk=pk)

        report = Report.objects.get(id=pk)
        report.delete()
        return redirect('panel:report:reports')

