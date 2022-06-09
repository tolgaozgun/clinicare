import datetime

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.timezone import now
from django.views import View
from .models import User, Prescription, Report
from .forms import RegisterForm, LoginForm, PrescriptionForm, ReportForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

PATIENT_ROLE = 1
DOCTOR_ROLE = 2


class DashboardView(View):
    def get(self, request):
        return render(request, 'panel/dashboard.html')


class DoctorsView(View):
    def get(self, request):
        try:
            doctors = User.objects.filter(role=DOCTOR_ROLE)
        except User.DoesNotExist:
            doctors = None
        context = {'doctors': doctors}
        return render(request, 'panel/doctors.html', context)


class PrescriptionsView(View):
    def get(self, request):
        try:
            prescriptions = Prescription.objects.filter()
        except Prescription.DoesNotExist:
            prescriptions = None

        context = {'prescriptions': prescriptions}
        return render(request, 'panel/prescriptions.html', context)


class ReportsView(View):
    def get(self, request):
        try:
            reports = Report.objects.filter()
        except Report.DoesNotExist:
            reports = None
        context = {'reports': reports}
        return render(request, 'panel/reports.html', context)


class PatientsView(View):
    def get(self, request):
        try:
            patients = User.objects.filter(role=PATIENT_ROLE)
        except User.DoesNotExist:
            patients = None
        context = {'patients': patients}
        return render(request, 'panel/patients.html', context)


class PrescriptionView(View):
    def get(self, request, pk):
        is_valid = False
        try:
            prescription = Prescription.objects.get(id=pk)
            is_valid = True
        except User.DoesNotExist:
            prescription = Prescription(doctor=None,
                                        patient=None,
                                        drugs=None,
                                        files=None,
                                        dateCreated=None,
                                        lastUpdated=None)
            is_valid = False # Failsafe
        context = {'is_valid': is_valid, 'prescription': prescription}
        return render(request, 'panel/prescription.html', context)


class ReportView(View):
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
        context = {'is_valid': is_valid, 'report': report}
        return render(request, 'panel/report.html', context)


class PatientView(View):
    def get(self, request, pk):
        is_valid = False
        try:
            patient = User.objects.get(id=pk, role=PATIENT_ROLE)
            is_valid = True
        except User.DoesNotExist:
            patient = User(username="N/A",
                           name=None,
                           surname=None,
                           email=None,
                           phone=None,
                           role=0,
                           department=None,
                           status=0,
                           isActivated=0,
                           is2FAEnabled=0,
                           lastLogin=None,
                           lastUpdated=None,
                           dateCreated=None)
            is_valid = False # Failsafe
        context = {'is_valid': is_valid, 'patient': patient}
        return render(request, 'panel/patient.html', context)


class DoctorView(View):
    def get(self, request, pk):
        is_valid = False
        try:
            doctor = User.objects.get(id=pk, role=DOCTOR_ROLE)
            is_valid = True
        except User.DoesNotExist:
            doctor = User(username="N/A",
                          name=None,
                          surname=None,
                          email=None,
                          phone=None,
                          role=0,
                          department=None,
                          status=0,
                          isActivated=0,
                          is2FAEnabled=0,
                          lastLogin=None,
                          lastUpdated=None,
                          dateCreated=None)
            is_valid = False # Failsafe
        context = {'is_valid': is_valid, 'doctor': doctor}
        return render(request, 'panel/doctor.html', context)


class AddPatientView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'panel/add_patient.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        # doctor_form = RegisterDoctorForm(request.POST)

        if form.is_valid():
            password_hashed = make_password(form.cleaned_data['password'])
            new_patient = User(name=form.cleaned_data['name'],
                               surname=form.cleaned_data['surname'],
                               email=form.cleaned_data['email'],
                               phone=form.cleaned_data['phone'],
                               status=1,
                               role=PATIENT_ROLE,
                               photo=None,
                               password=password_hashed,
                               isActivated=False,
                               is2FAEnabled=False,
                               lastLogin=None,
                               lastUpdated=now,
                               dateCreated=now)
            new_patient.save()
            return redirect('panel')
        else:
            return render(request, "panel/add_patient.html", {'form': form})


class AddDoctorView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'panel/add_doctor.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        # doctor_form = RegisterDoctorForm(request.POST)

        if form.is_valid():
            password_hashed = make_password(form.cleaned_data['password'])
            new_patient = User(name=form.cleaned_data['name'],
                               surname=form.cleaned_data['surname'],
                               email=form.cleaned_data['email'],
                               phone=form.cleaned_data['phone'],
                               status=1,
                               role=DOCTOR_ROLE,
                               photo=None,
                               password=password_hashed,
                               isActivated=False,
                               is2FAEnabled=False,
                               lastLogin=None,
                               lastUpdated=now,
                               dateCreated=now)
            new_patient.save()
            return redirect('panel')
        else:
            return render(request, "panel/add_doctor.html", {'form': form})


class AddReportView(View):
    def get(self, request):
        form = ReportForm()
        return render(request, 'panel/add_report.html', {'form': form})

    def post(self, request):
        form = ReportForm(request.POST)
        # doctor_form = RegisterDoctorForm(request.POST)

        if form.is_valid():
            new_report = Report(**form.cleaned_data,
                                dateCreated=now,
                                lastUpdated=now)
            new_report.save()
            return redirect('panel')
        else:
            return render(request, "panel/add_report.html", {'form': form})


class AddPrescriptionView(View):
    def get(self, request):
        form = PrescriptionForm()
        return render(request, 'panel/add_prescription.html', {'form': form})

    def post(self, request):
        form = PrescriptionForm(request.POST)
        # doctor_form = RegisterDoctorForm(request.POST)

        if form.is_valid():
            new_prescription = Prescription(**form.cleaned_data,
                                            dateCreated=now,
                                            lastUpdated=now)
            new_prescription.save()
            return redirect('panel')
        else:
            return render(request, "panel/add_prescription.html", {'form': form})
