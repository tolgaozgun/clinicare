from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.forms import ClearableFileInput
from .models import Report


class ReportForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    files = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Report
        fields = ['doctor', 'patient', 'type']

    def clean(self):
        super().clean()

        value_doctor = self.cleaned_data.get('doctor')
        value_patient = self.cleaned_data.get('patient')
        value_type = self.cleaned_data.get('type')
        value_files = self.cleaned_data.get('files')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'doctor': 'Select a doctor',
            'patient': 'Select a patient',
            'type': 'Enter report type',
            'files': 'Select files',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'
