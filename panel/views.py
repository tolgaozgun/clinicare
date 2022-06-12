import datetime

from clinic.settings import MEDIA_URL, MEDIA_ROOT
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.timezone import now
from django.views import View
from .models import User, Prescription, Report, Product
from .forms import RegisterForm, DoctorForm, PrescriptionForm, ReportForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

# Create your views here.

PATIENT_ROLE = 1
DOCTOR_ROLE = 2


class PanelView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect'


class DashboardView(PanelView):
    def get(self, request):
        context = {'current_page': 'home'}
        return render(request, 'panel/dashboard.html', context)


class DoctorsView(PanelView):
    def get(self, request):
        try:
            doctors = User.objects.filter(role=DOCTOR_ROLE)
        except User.DoesNotExist:
            doctors = None
        context = {'doctors': doctors, 'current_page': 'doctors'}
        return render(request, 'panel/doctors.html', context)


class PrescriptionsView(PanelView):
    def get(self, request):
        try:
            prescriptions = Prescription.objects.filter()
        except Prescription.DoesNotExist:
            prescriptions = None

        context = {'prescriptions': prescriptions, 'current_page': 'prescriptions'}
        return render(request, 'panel/prescriptions.html', context)


class ReportsView(PanelView):
    def get(self, request):
        try:
            reports = Report.objects.filter()
        except Report.DoesNotExist:
            reports = None
        context = {'reports': reports, 'current_page': 'reports'}
        return render(request, 'panel/reports.html', context)


class PatientsView(PanelView):
    def get(self, request):
        try:
            patients = User.objects.filter(role=PATIENT_ROLE)
        except User.DoesNotExist:
            patients = None
        context = {'patients': patients, 'current_page': 'patients'}
        return render(request, 'panel/patients.html', context)


class PrescriptionView(PanelView):
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
            is_valid = False  # Failsafe

        print("MEDIA_URL")
        print(MEDIA_URL)
        print("MEDIA_ROOT")
        print(MEDIA_ROOT)
        context = {'is_valid': is_valid, 'current_page': 'view_prescription', 'prescription': prescription, "MEDIA_ROOT": MEDIA_URL}
        return render(request, 'panel/prescription.html', context)


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
        context = {'is_valid': is_valid, 'current_page': 'view_report', 'report': report}
        return render(request, 'panel/report.html', context)


class PatientView(PanelView):
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
            is_valid = False  # Failsafe
        context = {'is_valid': is_valid, 'current_page': 'view_patient', 'patient': patient}
        return render(request, 'panel/patient.html', context)


class DoctorView(PanelView):
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
            is_valid = False  # Failsafe
        context = {'is_valid': is_valid, 'current_page': 'view_doctor', 'doctor': doctor}
        return render(request, 'panel/doctor.html', context)


class AddPatientView(PanelView):
    def get(self, request):
        form = RegisterForm()
        context = {"current_page": "add_patient", "form": form}
        return render(request, 'panel/add_patient.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)

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
            context = {"current_page": "add_patient", "form": form}
            return render(request, "panel/add_patient.html", context)


class AddDoctorView(PanelView):
    def get(self, request):
        form = DoctorForm()
        context = {"current_page": "add_doctor", "form": form}
        return render(request, 'panel/add_doctor.html', context)

    def post(self, request):
        form = DoctorForm(request.POST)
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
            context = {"current_page": "add_doctor", "form": form}
            return render(request, "panel/add_doctor.html", context)


class AddReportView(PanelView):
    def get(self, request):
        form = ReportForm()
        context = {"current_page": "add_report", "form": form}
        return render(request, 'panel/add_report.html', context)

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
            context = {"current_page": "add_report", "form": form}
            return render(request, "panel/add_report.html", context)


class AddPrescriptionView(PanelView):
    def get(self, request):
        form = PrescriptionForm()
        context = {'current_page': 'add_prescription', 'form': form}
        return render(request, 'panel/add_prescription.html', context)

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
            context = {"current_page": "add_prescription", "form": form}
            return render(request, "panel/add_prescription.html", context)


class EditPatientView(PanelView):
    def get(self, request, pk):
        is_valid = False
        try:
            patient = User.objects.get(id=pk, role=PATIENT_ROLE)
            is_valid = True
        except User.DoesNotExist:
            patient = None

        form = RegisterForm(instance=patient)
        context = {"current_page": "edit_patient", "form": form, "is_valid": is_valid}
        return render(request, 'panel/add_patient.html', context)

    def post(self, request, pk):
        is_valid = False
        try:
            patient = User.objects.get(id=pk, role=PATIENT_ROLE)
            is_valid = True
        except User.DoesNotExist:
            patient = None

        form = RegisterForm(request.POST, instance=patient)

        if form.is_valid() and is_valid:
            # password_hashed = make_password(form.cleaned_data['password'])
            new_patient = User(name=form.cleaned_data['name'],
                               surname=form.cleaned_data['surname'],
                               email=form.cleaned_data['email'],
                               phone=form.cleaned_data['phone'],
                               status=form.cleaned_data['status'],
                               role=PATIENT_ROLE,
                               photo=form.cleaned_data['photo'],
                               password=patient.password,
                               isActivated=form.cleaned_data['isActivated'],
                               is2FAEnabled=form.cleaned_data['is2FAEnabled'],
                               lastLogin=form.cleaned_data['lastLogin'],
                               lastUpdated=now,
                               dateCreated=patient.dateCreated)
            new_patient.save()
            return redirect('panel')
        else:
            context = {'current_page': 'edit_patient', 'form': form}
            return render(request, "panel/add_patient.html", context)


class EditDoctorView(PanelView):
    def get(self, request, pk):
        is_valid = False
        try:
            doctor = User.objects.get(id=pk, role=DOCTOR_ROLE)
            is_valid = True
        except User.DoesNotExist:
            doctor = None

        form = RegisterForm(instance=doctor)
        context = {"form": form, "is_valid": is_valid, 'current_page': 'edit_doctor'}
        return render(request, 'panel/add_doctor.html', context)

    def post(self, request, pk):
        form = RegisterForm(request.POST)
        is_valid = False
        try:
            doctor = User.objects.get(id=pk, role=DOCTOR_ROLE)
            is_valid = True
        except User.DoesNotExist:
            doctor = None

        if form.is_valid() and is_valid:
            password_hashed = make_password(form.cleaned_data['password'])
            new_doctor = User(name=form.cleaned_data['name'],
                              surname=form.cleaned_data['surname'],
                              email=form.cleaned_data['email'],
                              phone=form.cleaned_data['phone'],
                              status=form.cleaned_data['status'],
                              department=form.cleaned_data['department'],
                              role=DOCTOR_ROLE,
                              photo=form.cleaned_data['photo'],
                              password=doctor.password,
                              isActivated=form.cleaned_data['isActivated'],
                              is2FAEnabled=form.cleaned_data['is2FAEnabled'],
                              lastLogin=form.cleaned_data['lastLogin'],
                              lastUpdated=now,
                              dateCreated=doctor.dateCreated)
            new_doctor.save()
            return redirect('panel')
        else:
            context = {'current_page': 'edit_doctor', 'form': form}
            return render(request, "panel/add_doctor.html", context)


class EditReportView(PanelView):
    def get(self, request, pk):
        form = ReportForm()
        context = {'current_page': 'edit_report', 'form': form}
        return render(request, 'panel/add_report.html', context)

    def post(self, request, pk):
        form = ReportForm(request.POST)
        # doctor_form = RegisterDoctorForm(request.POST)

        if form.is_valid():
            new_report = Report(**form.cleaned_data,
                                dateCreated=now,
                                lastUpdated=now)
            new_report.save()
            return redirect('panel')
        else:
            context = {'current_page': 'edit_report', 'form': form}
            return render(request, "panel/add_report.html", context)


class EditPrescriptionView(PanelView):
    def get(self, request, pk):
        form = PrescriptionForm()
        context = {'current_page': 'edit_prescription',
                   'form': form}
        return render(request, 'panel/add_prescription.html', context)

    def post(self, request, pk):
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


class ProductsView(View):
    def get(self, request):
        return render(request, 'panel/products.html')


class ProductView(View):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            product = None

        context = {'product': product}
        return render(request, 'panel/product.html', context)
