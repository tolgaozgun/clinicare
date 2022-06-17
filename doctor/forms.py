import phonenumbers
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from accounts.models import User


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


