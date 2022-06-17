from accounts.forms import RegisterForm
from appointment.models import Appointment
from clinic.settings import MODELS_PER_PAGE
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.timezone import now
from accounts.models import User
from panel.roles import Roles
from panel.views import PanelView
from patient.forms import EditPatientForm
from prescription.models import Prescription
from report.models import Report


class EditPatientView(PanelView):
    def get(self, request, pk):
        is_valid = False
        try:
            patient = User.objects.get(id=pk, role=Roles.PATIENT.value)
            is_valid = True
        except User.DoesNotExist:
            patient = None

        form = EditPatientForm(instance=patient)
        context = {"current_page": "edit_patient", "form": form, "is_valid": is_valid}
        return render(request, 'patient/edit_patient.html', context)

    def post(self, request, pk):
        is_valid = False
        try:
            patient = User.objects.get(id=pk, role=Roles.PATIENT.value)
            is_valid = True
        except User.DoesNotExist:
            patient = None

        form = EditPatientForm(request.POST, instance=patient)

        if form.is_valid() and is_valid:
            if len(str(form.cleaned_data['password'])) > 0:
                password_hashed = make_password(form.cleaned_data['password'])
            else:
                password_hashed = patient.password
            patient.password = password_hashed
            patient.lastUpdated = now
            patient.save()
            return redirect('panel:patient:patients')
        else:
            print("Is valid " + str(form.is_valid()))
            print("errors " + str(form.errors.as_data()))
            context = {'current_page': 'edit_patient', 'form': form}
            return render(request, "patient/edit_patient.html", context)


class AddPatientView(PanelView):
    def get(self, request):
        form = RegisterForm()
        context = {"current_page": "add_patient", "form": form}
        return render(request, 'patient/add_patient.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            password_hashed = make_password(form.cleaned_data['password'])
            new_patient = User(first_name=form.cleaned_data['first_name'],
                               last_name=form.cleaned_data['last_name'],
                               email=form.cleaned_data['email'],
                               phone=form.cleaned_data['phone'],
                               status=1,
                               role=Roles.PATIENT.value,
                               photo=None,
                               password=password_hashed,
                               is_active=False,
                               is2FAEnabled=False,
                               lastLogin=None,
                               lastUpdated=now,
                               dateCreated=now)
            new_patient.save()
            return redirect('panel:patient:patients')
        else:
            context = {"current_page": "add_patient", "form": form}
            return render(request, "patient/add_patient.html", context)


class PatientsView(PanelView):
    def get(self, request):
        patients = User.objects.filter(role=Roles.PATIENT.value)
        paginator = Paginator(patients, MODELS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'patients': page_obj, 'current_page': 'patients'}
        return render(request, 'patient/patients.html', context)


class PatientView(PanelView):
    def get(self, request, pk):
        is_valid = False
        try:
            patient = User.objects.get(id=pk, role=Roles.PATIENT.value)
            is_valid = True
        except User.DoesNotExist:
            patient = User(first_name=None,
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

        prescriptions = Prescription.objects.filter(patient=patient)
        reports = Report.objects.filter(doctor=patient)
        appointments = Appointment.objects.filter(doctor=patient)
        context = {'is_valid': is_valid, 'current_page': 'view_patient', 'patient': patient,
                   'prescriptions': prescriptions, 'reports': reports, 'appointments': appointments}
        return render(request, 'patient/patient.html', context)


class DeletePatientView(PanelView):
    def get(self, request, pk):
        context = {'current_page': 'delete_patient'}
        return render(request, 'patient/delete_patient.html', context)

    def post(self, request, pk):
        if 'answer_no' in request.POST:
            return redirect('panel:patient:patient', pk)

        patient = User.objects.get(id=pk)
        patient.delete()
        return redirect('panel:patient:patients')
