from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.utils import timezone
from .models import Appointment


class AddAppointmentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointmentDate']

    def clean(self):
        value_doctor = self.cleaned_data.get('doctor')
        value_patient = self.cleaned_data.get('patient')
        value_appointment_date = self.cleaned_data.get('appointmentDate')

        if value_appointment_date < timezone.now().date():
            raise forms.ValidationError("Appointment date cannot be before today.")

        # Check if doctor and patient exists

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(AddAppointmentForm, self).__init__(*args, **kwargs)
        placeholders = {
            'doctor': 'Select the doctor',
            'patient': 'Select the patient',
            'appointmentDate': 'Select the date for appointment',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'
