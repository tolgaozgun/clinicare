from django import forms
from panel.models import User
import phonenumbers
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    email = forms.EmailField(widget=forms.EmailInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'example@email.com',
            'password': 'Password',
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
