from clinic.settings import MODELS_PER_PAGE
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import now
from panel.roles import Roles

from .forms import PrescriptionForm
from .models import Prescription, User, PrescriptionFile
from panel.views import PanelView


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
            return redirect('panel:prescription:prescriptions')
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
            return redirect('panel:prescription:prescriptions')
        else:
            print(form.errors.as_data())
            return render(request, "prescription/add_prescription.html", {'form': form})


class DeletePrescriptionView(PanelView):
    def get(self, request, pk):
        context = {'current_page': 'delete_prescription'}
        return render(request, 'prescription/delete_prescription.html', context)

    def post(self, request, pk):
        if 'answer_no' in request.POST:
            return redirect('panel:prescription:prescription', pk)

        prescription = Prescription.objects.get(id=pk)
        prescription.delete()
        return redirect('panel:prescription:prescriptions')