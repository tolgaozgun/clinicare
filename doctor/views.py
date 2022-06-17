from appointment.models import Appointment
from clinic.settings import MODELS_PER_PAGE
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.timezone import now
from panel.roles import Roles
from prescription.models import Prescription
from report.models import Report

from .forms import DoctorForm
from accounts.models import User
from panel.views import PanelView


class DoctorsView(PanelView):
    def get(self, request):
        doctors = User.objects.filter(role=Roles.DOCTOR.value)
        paginator = Paginator(doctors, MODELS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'doctors': page_obj, 'current_page': 'doctors'}
        return render(request, 'doctor/doctors.html', context)


class DoctorView(PanelView):
    def get(self, request, pk):
        is_valid = False
        try:
            doctor = User.objects.get(id=pk, role=Roles.DOCTOR.value)
            is_valid = True
        except User.DoesNotExist:
            doctor = User(first_name=None,
                          last_name=None,
                          email=None,
                          phone=None,
                          role=0,
                          department=None,
                          status=0,
                          is_active=False,
                          is2FAEnabled=0,
                          lastLogin=None,
                          lastUpdated=None,
                          dateCreated=None)
            is_valid = False  # Failsafe
        prescriptions = Prescription.objects.filter(doctor=doctor)
        reports = Report.objects.filter(doctor=doctor)
        appointments = Appointment.objects.filter(doctor=doctor)
        context = {'is_valid': is_valid, 'current_page': 'view_doctor', 'doctor': doctor,
                   'appointments': appointments, 'reports': reports, 'prescriptions': prescriptions}
        return render(request, 'doctor/doctor.html', context)


class EditDoctorView(PanelView):
    def get(self, request, pk):
        is_valid = False
        try:
            doctor = User.objects.get(id=pk, role=Roles.DOCTOR.value)
            is_valid = True
        except User.DoesNotExist:
            doctor = None

        form = DoctorForm(instance=doctor)
        context = {"form": form, "is_valid": is_valid, 'current_page': 'edit_doctor'}
        return render(request, 'doctor/add_doctor.html', context)

    def post(self, request, pk):
        is_valid = False
        try:
            doctor = User.objects.get(id=pk, role=Roles.DOCTOR.value)
            is_valid = True
        except User.DoesNotExist:
            doctor = None
        form = DoctorForm(request.POST, instance=doctor)

        if form.is_valid() and is_valid:
            if len(str(form.cleaned_data['password'])) > 0:
                password_hashed = make_password(form.cleaned_data['password'])
            else:
                password_hashed = doctor.password
            doctor.password = password_hashed
            doctor.lastUpdated = now
            doctor.save()
            return redirect('panel:doctor:doctors')
        else:
            context = {'current_page': 'edit_doctor', 'form': form}
            return render(request, "doctor/add_doctor.html", context)


class AddDoctorView(PanelView):
    def get(self, request):
        form = DoctorForm()
        context = {"current_page": "add_doctor", "form": form}
        return render(request, 'doctor/add_doctor.html', context)

    def post(self, request):
        form = DoctorForm(request.POST, request.FILES)

        if form.is_valid():
            password_hashed = make_password(form.cleaned_data['password'])
            form.cleaned_data.pop('confirmPassword')
            form.cleaned_data.pop('captcha')
            form.cleaned_data['password'] = password_hashed

            new_doctor = User(**form.cleaned_data,
                              role=Roles.DOCTOR.value,
                              # photo=request.FILES['photo'],
                              lastLogin=None,
                              lastUpdated=now,
                              dateCreated=now)
            new_doctor.save()
            return redirect('panel:doctor:doctors')
        else:
            context = {"current_page": "add_doctor", "form": form}
            return render(request, "doctor/add_doctor.html", context)
