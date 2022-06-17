from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.forms import ClearableFileInput
from .models import Prescription


class PrescriptionForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    files = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Prescription
        fields = ['doctor', 'patient', 'drugs']

    def clean(self):
        super().clean()

        # value_doctor = self.cleaned_data.get('doctor')
        # value_patient = self.cleaned_data.get('patient')
        # value_drugs = self.cleaned_data.get('drugs')
        # value_files = self.cleaned_data.get('files')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'doctor': 'Select a doctor',
            'patient': 'Select a patient',
            'drugs': 'Enter prescribed drugs',
            'files': 'Select files',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'

