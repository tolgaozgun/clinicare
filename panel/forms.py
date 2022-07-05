import phonenumbers
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.forms import ClearableFileInput
from django.utils import timezone
from accounts.models import User

from .models import Prescription, Report, Product, Appointment


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


class AddProductForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    images = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price']
                  # 'coverImage']

    def clean(self):
        super(AddProductForm, self).clean()

        value_name = self.cleaned_data.get('name')
        value_slug = self.cleaned_data.get('slug')
        value_desc = self.cleaned_data.get('description')
        value_price = self.cleaned_data.get('price')
        value_image = self.cleaned_data.get('images')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Product name',
            'slug': 'Product url',
            'description': 'Product description',
            'price': 'Price',
            # 'coverImage': 'Cover Image',
            'images': 'Product Images',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'


class EditProductForm(forms.ModelForm):
    images = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price']

    def clean(self):
        super(EditProductForm, self).clean()

        value_name = self.cleaned_data.get('name')
        value_slug = self.cleaned_data.get('slug')
        value_desc = self.cleaned_data.get('description')
        value_price = self.cleaned_data.get('price')
        value_image = self.cleaned_data.get('images')


class AddAppointmentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointmentDate']
        widgets = {
            'appointmentDate': forms.DateTimeInput(attrs={'disabled': ''})
        }

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


class DoctorAddAppointmentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Appointment
        fields = ['appointmentDate']
        widgets = {
            'appointmentDate': forms.DateTimeInput(attrs={'readonly': 'readonly'})
        }

    def clean(self):
        value_appointment_date = self.cleaned_data.get('appointmentDate')

        if value_appointment_date < timezone.now():
            raise forms.ValidationError("Appointment date cannot be before today.")

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(DoctorAddAppointmentForm, self).__init__(*args, **kwargs)
        placeholders = {
            'appointmentDate': 'Select the date for appointment',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(render_value=True))
    confirmEmail = forms.EmailField(widget=forms.EmailInput())
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean(self):
        super(RegisterForm, self).clean()

        value_name = self.cleaned_data.get('first_name')
        value_surname = self.cleaned_data.get('last_name')
        value_email = self.cleaned_data.get('email')
        value_confirm_email = self.cleaned_data.get('confirmEmail')
        value_phone = self.cleaned_data.get('phone')
        value_password = self.cleaned_data.get('password')
        value_confirm_password = self.cleaned_data.get('confirmPassword')

        if value_password != value_confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match!'])
            self._errors['confirmPassword'] = self.error_class(['Passwords do not match!'])

        if len(str(value_password).strip()) < 8:
            self._errors['password'] = self.error_class(['Password cannot be smaller than 8 digits.'])
            self._errors['confirmPassword'] = self.error_class(['Password cannot be smaller than 8 digits.'])

        if len(str(value_password).strip()) > 16:
            self._errors['password'] = self.error_class(['Password cannot be higher than 16 digits.'])
            self._errors['confirmPassword'] = self.error_class(['Password cannot be smaller 16 digits.'])

        if value_email != value_confirm_email:
            self._errors['email'] = self.error_class(['Email addresses do not match!'])
            self._errors['confirmEmail'] = self.error_class(['Email addresses do not match!'])

        if len(str(value_name).strip()) < 1:
            self._errors['first_name'] = self.error_class(['Please enter your first name'])

        if len(str(value_surname).strip()) < 1:
            self._errors['last_name'] = self.error_class(['Please enter your last name'])

        phone = phonenumbers.parse(str(value_phone))

        if not phonenumbers.is_possible_number(phone):
            self._errors['phone'] = self.error_class(['Please enter a valid phone number'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'example@email.com',
            'confirmEmail': 'example@email.com',
            'phone': '+905123456789',
            'password': 'Password',
            'confirmPassword': 'Confirm Password',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'

class EditPatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(render_value=True))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'status', 'is_active',
                  'is2FAEnabled', 'photo']

    def clean(self):
        super(EditPatientForm, self).clean()

        value_name = self.cleaned_data.get('first_name')
        value_surname = self.cleaned_data.get('last_name')
        value_email = self.cleaned_data.get('email')
        value_phone = self.cleaned_data.get('phone')
        value_password = self.cleaned_data.get('password')
        value_confirm_password = self.cleaned_data.get('confirmPassword')

        if value_password != value_confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match!'])
            self._errors['confirmPassword'] = self.error_class(['Passwords do not match!'])

        if len(str(value_password)) > 0:
            if len(str(value_password).strip()) < 8:
                self._errors['password'] = self.error_class(['Password cannot be smaller than 8 digits.'])
                self._errors['confirmPassword'] = self.error_class(['Password cannot be smaller than 8 digits.'])

            if len(str(value_password).strip()) > 16:
                self._errors['password'] = self.error_class(['Password cannot be higher than 16 digits.'])
                self._errors['confirmPassword'] = self.error_class(['Password cannot be smaller 16 digits.'])

        if len(str(value_name).strip()) < 1:
            self._errors['first_name'] = self.error_class(['Please enter your first name'])

        if len(str(value_surname).strip()) < 1:
            self._errors['last_name'] = self.error_class(['Please enter your last name'])

        phone = phonenumbers.parse(str(value_phone))

        if not phonenumbers.is_possible_number(phone):
            self._errors['phone'] = self.error_class(['Please enter a valid phone number'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'example@email.com',
            'phone': '+905123456789',
            'password': 'Password',
            'confirmPassword': 'Confirm Password',
            'status': 'Select status',
            'is_active': 'Change if the account is activated',
            'is2FAEnabled': 'Change the 2FA status of this account',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'



class DoctorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(render_value=True))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'status', 'department',
                  'photo', 'is_active', 'is2FAEnabled']


    def clean(self):
        super(DoctorForm, self).clean()

        value_name = self.cleaned_data.get('first_name')
        value_surname = self.cleaned_data.get('last_name')
        value_email = self.cleaned_data.get('email')
        value_phone = self.cleaned_data.get('phone')
        value_password = self.cleaned_data.get('password')
        value_confirm_password = self.cleaned_data.get('confirmPassword')

        if value_password != value_confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match!'])
            self._errors['confirmPassword'] = self.error_class(['Passwords do not match!'])

        if len(str(value_password)) > 0:
            if len(str(value_password).strip()) < 8:
                self._errors['password'] = self.error_class(['Password cannot be smaller than 8 digits.'])
                self._errors['confirmPassword'] = self.error_class(['Password cannot be smaller than 8 digits.'])

            if len(str(value_password).strip()) > 16:
                self._errors['password'] = self.error_class(['Password cannot be higher than 16 digits.'])
                self._errors['confirmPassword'] = self.error_class(['Password cannot be smaller 16 digits.'])

        if len(str(value_name).strip()) < 1:
            self._errors['first_name'] = self.error_class(['Please enter your first name'])

        if len(str(value_surname).strip()) < 1:
            self._errors['last_name'] = self.error_class(['Please enter your last name'])

        phone = phonenumbers.parse(str(value_phone))

        if not phonenumbers.is_possible_number(phone):
            self._errors['phone'] = self.error_class(['Please enter a valid phone number'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'example@email.com',
            'phone': '+905123456789',
            'password': 'Password',
            'confirmPassword': 'Confirm Password',
            'status': 'Select status',
            'department': 'Enter a department',
            'is_active': 'Change if the account is activated',
            'is2FAEnabled': 'Change the 2FA status of this account',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'


class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(render_value=True))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'role', 'department', 'status', 'is_active',
                  'is2FAEnabled', 'photo']

    def clean(self):
        super(EditUserForm, self).clean()

        value_name = self.cleaned_data.get('first_name')
        value_surname = self.cleaned_data.get('last_name')
        value_email = self.cleaned_data.get('email')
        value_phone = self.cleaned_data.get('phone')
        value_password = self.cleaned_data.get('password')
        value_confirm_password = self.cleaned_data.get('confirmPassword')

        if value_password != value_confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match!'])
            self._errors['confirmPassword'] = self.error_class(['Passwords do not match!'])

        if len(str(value_password)) > 0:
            if len(str(value_password).strip()) < 8:
                self._errors['password'] = self.error_class(['Password cannot be smaller than 8 digits.'])
                self._errors['confirmPassword'] = self.error_class(['Password cannot be smaller than 8 digits.'])

            if len(str(value_password).strip()) > 16:
                self._errors['password'] = self.error_class(['Password cannot be higher than 16 digits.'])
                self._errors['confirmPassword'] = self.error_class(['Password cannot be smaller 16 digits.'])

        if len(str(value_name).strip()) < 1:
            self._errors['first_name'] = self.error_class(['Please enter your first name'])

        if len(str(value_surname).strip()) < 1:
            self._errors['last_name'] = self.error_class(['Please enter your last name'])

        phone = phonenumbers.parse(str(value_phone))

        if not phonenumbers.is_possible_number(phone):
            self._errors['phone'] = self.error_class(['Please enter a valid phone number'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'example@email.com',
            'phone': '+905123456789',
            'password': 'New Password',
            'confirmPassword': 'Confirm New Password',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'




