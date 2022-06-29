from accounts.models import User
from clinic.settings import MODELS_PER_PAGE
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.timezone import now
from panel.roles import Roles

from .forms import AddAppointmentForm, DoctorAddAppointmentForm
from .models import Appointment
from panel.views import PanelView


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
            return redirect('panel:appointment:appointments')
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
