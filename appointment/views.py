from accounts.models import User
from clinic.settings import MODELS_PER_PAGE
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.timezone import now
from panel.roles import Roles

from .forms import AddAppointmentForm
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
        context = {'current_page': 'add_appointment', 'form': form}
        form.fields['patient'].queryset = User.objects.filter(role=Roles.PATIENT.value)
        form.fields['doctor'].queryset = User.objects.filter(role=Roles.DOCTOR.value)
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