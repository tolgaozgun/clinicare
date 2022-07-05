from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from clinic.settings import MODELS_PER_PAGE
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import now
from panel.roles import Roles
from .models import Report, Appointment, Prescription, PrescriptionFile, Product, ProductImage, ReportFile
from .forms import PrescriptionForm, AddProductForm, AddAppointmentForm, DoctorAddAppointmentForm, ReportForm
from accounts.models import User

class PanelView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect'


class DashboardView(PanelView):
    def get(self, request):
        context = {'current_page': 'home'}
        return render(request, 'panel/dashboard.html', context)


class MessagingView(PanelView):
    def get(self, request):
        context = {'current_page': 'messaging'}
        return render(request, 'panel/messaging.html', context)


# Prescription Views


class PrescriptionsView(PanelView):
    def get(self, request):
        prescriptions = Prescription.objects.all()
        paginator = Paginator(prescriptions, MODELS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'prescriptions': page_obj, 'current_page': 'prescriptions'}
        return render(request, 'prescription/prescriptions.html', context)


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
        prescription.files = prescription.prescription_file_prescription.all()
        context = {'is_valid': is_valid, 'current_page': 'view_prescription', 'prescription': prescription}
        return render(request, 'prescription/prescription.html', context)


class AddPrescriptionView(PanelView):
    def get(self, request):
        form = PrescriptionForm()
        form.fields['patient'].queryset = User.objects.filter(role=Roles.PATIENT.value)
        form.fields['doctor'].queryset = User.objects.filter(role=Roles.DOCTOR.value)
        context = {'current_page': 'add_prescription', 'form': form}
        return render(request, 'prescription/add_prescription.html', context)

    def post(self, request):
        form = PrescriptionForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            form.cleaned_data.pop('files')
            form.cleaned_data.pop('captcha')
            new_prescription = Prescription(**form.cleaned_data,
                                            dateCreated=now,
                                            lastUpdated=now)
            new_prescription.save()
            for f in files:
                file = PrescriptionFile(file=f, prescription=new_prescription)
                file.save()
            return redirect('')
        else:
            context = {"current_page": "add_prescription", "form": form}
            return render(request, "prescription/add_prescription.html", context)


class EditPrescriptionView(PanelView):
    def get(self, request, pk):

        prescription = Prescription.objects.get(id=pk)
        form = PrescriptionForm(instance=prescription)
        form.fields['patient'].queryset = User.objects.filter(role=Roles.PATIENT.value)
        form.fields['doctor'].queryset = User.objects.filter(role=Roles.DOCTOR.value)
        context = {'current_page': 'edit_prescription', 'form': form}
        return render(request, 'prescription/add_prescription.html', context)

    def post(self, request, pk):
        prescription = Prescription.objects.get(id=pk)
        form = PrescriptionForm(request.POST, request.FILES, instance=prescription)
        files = request.FILES.getlist('files')
        if form.is_valid():
            form.cleaned_data.pop('files')
            form.cleaned_data.pop('captcha')
            prescription.lastUpdated = now
            prescription.save()
            for f in files:
                file = PrescriptionFile(file=f, prescription=prescription)
                file.save()
            return redirect('panel:prescriptions')
        else:
            print(form.errors.as_data())
            return render(request, "prescription/add_prescription.html", {'form': form})


class DeletePrescriptionView(PanelView):
    def get(self, request, pk):
        context = {'current_page': 'delete_prescription'}
        return render(request, 'prescription/delete_prescription.html', context)

    def post(self, request, pk):
        if 'answer_no' in request.POST:
            return redirect('panel:prescription', pk)

        prescription = Prescription.objects.get(id=pk)
        prescription.delete()
        return redirect('panel:prescriptions')


# Report Views

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
            return redirect('panel:reports')
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
            return redirect('panel:reports')
        else:
            context = {'current_page': 'edit_report', 'form': form}
            return render(request, "report/add_report.html", context)


class DeleteReportView(PanelView):
    def get(self, request, pk):
        context = {'current_page': 'delete_report'}
        return render(request, 'report/delete_report.html', context)

    def post(self, request, pk):
        if 'answer_no' in request.POST:
            return redirect('panel:report', pk=pk)

        report = Report.objects.get(id=pk)
        report.delete()
        return redirect('panel:reports')


# Product Views



class ProductView(PanelView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            is_valid = True
        except Product.DoesNotExist:
            product = None
            is_valid = False

        product.images = product.product_image_product.all()
        context = {'product': product, 'current_page': 'view_product', 'is_valid': is_valid}
        return render(request, 'product/product.html', context)


class ProductsView(PanelView):
    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, MODELS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'products': page_obj, 'current_page': 'products'}
        return render(request, 'product/products.html', context)


class DeleteProductView(PanelView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            product = None
        context = {'product': product, 'current_page': 'delete_product'}
        return render(request, 'product/delete_product.html', context)

    def post(self, request, pk):
        if 'answer_no' in request.POST:
            return redirect('panel:product', pk)

        product = Product.objects.get(id=pk)
        product.delete()
        return redirect('panel:products')


class AddProductView(PanelView):
    def get(self, request):
        form = AddProductForm()
        context = {'form': form, 'current_page': 'add_product'}
        return render(request, 'product/add_product.html', context)

    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            form.cleaned_data.pop('images')
            form.cleaned_data.pop('captcha')
            new_product = Product(**form.cleaned_data,
                                  dateCreated=now,
                                  lastUpdated=now)
            new_product.save()
            for f in images:
                image = ProductImage(file=f, product=new_product)
                image.save()
            return redirect('panel:products')
        else:
            context = {'current_page': 'add_product', 'form': form}
            return render(request, 'product/add_product.html', context)


class EditProductView(PanelView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            product = None

        form = AddProductForm(instance=product)
        context = {'form': form, 'current_page': 'edit_product'}
        return render(request, 'product/edit_product.html', context)

    def post(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            product = None
        form = AddProductForm(request.POST, request.FILES, instance=product)
        images = request.FILES.getlist('images')
        if form.is_valid():
            form.cleaned_data.pop('images')
            form.cleaned_data.pop('captcha')

            product.save()
            for f in images:
                image = ProductImage(file=f, product=product)
                image.save()
            return redirect('panel:products')
        else:
            context = {'current_page': 'add_product', 'form': form}
            return render(request, 'product/add_product.html', context)


# Appointment Views



class AppointmentsView(PanelView):
    def get(self, request):
        if request.user.role == Roles.PATIENT:
            appointments = Appointment.objects.filter(patient=request.user)
        else:
            appointments = Appointment.objects.all()
        paginator = Paginator(appointments, MODELS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'appointments': page_obj, 'current_page': 'appointments'}
        return render(request, 'appointment/appointments.html', context)


class AppointmentView(PanelView):
    def get(self, request, pk):
        appointments = Appointment.objects.get(id=pk)
        context = {'appointment': appointments, 'current_page': 'appointment'}
        return render(request, 'appointment/appointment.html', context)


class AddAppointmentView(PanelView):
    def get(self, request):
        form = AddAppointmentForm()
        j = 0
        i = 8
        times = []
        while i < 17:
            times.append(to_double_digits(i) + "." + to_double_digits(j))
            j += 15
            if j == 60:
                j = 0
                i += 1
        names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dates = ["19.07.2021", "20.07.2021", "21.07.2021", "22.07.2021", "23.07.2021", "24.07.2021", "25.07.2021"]
        days = {"names": names, "dates": dates}
        context = {'current_page': 'add_appointment', 'form': form, 'times': times, "days": days}
        form.fields['patient'].queryset = User.objects.filter(role=Roles.PATIENT.value)
        form.fields['patient'].queryset = User.objects.filter(role=Roles.PATIENT.value)
        return render(request, 'appointment/add_appointment.html', context)

    def post(self, request):
        form = AddAppointmentForm(request.POST)
        if form.is_valid():
            new_appointment = Appointment(**form.cleaned_data,
                                          dateCreated=now,
                                          lastUpdated=None)
            new_appointment.save()
            return redirect('appointments')
        else:
            context = {'current_page': 'add_appointment', 'form': form}
            return render(request, 'appointment/add_appointment.html', context)


class DoctorAddAppointmentView(PanelView):
    def get(self, request, pk):
        form = DoctorAddAppointmentForm()
        try:
            doctor = User.objects.filter(id=pk, role=Roles.DOCTOR.value).get()
        except User.DoesNotExist:
            doctor = None

        j = 0
        i = 8
        times = []
        while i < 17:
            times.append(to_double_digits(i) + "." + to_double_digits(j))
            j += 15
            if j == 60:
                j = 0
                i += 1
        names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        dates = ["19.07.2021", "20.07.2021", "21.07.2021", "22.07.2021", "23.07.2021", "24.07.2021", "25.07.2021"]
        days = {"names": names, "dates": dates}
        context = {'current_page': 'add_appointment', 'form': form, 'times': times, "days": days, "doctor": doctor,
                   'available': doctor.get_availability}
        return render(request, 'appointment/doctor_add_appointment.html', context)

    def post(self, request, pk):
        form = DoctorAddAppointmentForm(request.POST)
        try:
            doctor = User.objects.filter(id=pk, role=Roles.DOCTOR.value).get()
        except User.DoesNotExist:
            doctor = None

        if form.is_valid():
            form.cleaned_data.pop("captcha")
            new_appointment = Appointment(**form.cleaned_data,
                                          doctor=doctor,
                                          patient=request.user,
                                          dateCreated=now,
                                          lastUpdated=None)
            new_appointment.save()
            return redirect('panel:appointments')
        else:
            j = 0
            i = 8
            times = []
            while i < 17:
                times.append(to_double_digits(i) + "." + to_double_digits(j))
                j += 15
                if j == 60:
                    j = 0
                    i += 1
            names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

            dates = ["19.07.2021", "20.07.2021", "21.07.2021", "22.07.2021", "23.07.2021", "24.07.2021", "25.07.2021"]
            days = {"names": names, "dates": dates}
            context = {'current_page': 'add_appointment', 'form': form, 'times': times, "days": days, "doctor": doctor,
                       'available': doctor.get_availability}
            print(form.errors.as_data())
            return render(request, 'appointment/doctor_add_appointment.html', context)


def to_double_digits(value):
    value_str = str(value)
    if len(value_str) < 2:
        value_str = "0" + value_str
    return value_str


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
            return redirect('panel:patients')
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
            return redirect('panel:patients')
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
            return redirect('panel:patient', pk)

        patient = User.objects.get(id=pk)
        patient.delete()
        return redirect('panel:patients')


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
            return redirect('panel:doctors')
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
            return redirect('panel:doctors')
        else:
            context = {"current_page": "add_doctor", "form": form}
            return render(request, "doctor/add_doctor.html", context)

