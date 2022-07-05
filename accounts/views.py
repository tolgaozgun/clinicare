from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views import View
from accounts.models import User
from .forms import RegisterForm, LoginForm, ActivateForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django_email_verification import send_email


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            value_email = form.cleaned_data['email']
            value_password = form.cleaned_data['password']

            try:
                User.objects.get(email=value_email)
            except User.DoesNotExist:
                messages.error(request, "No user found.")

            user = authenticate(request, email=value_email, password=value_password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, "Your account is not activated!")
                    return render(request, "accounts/login.html", {'form': form})
            else:
                messages.error(request, "Password invalid.")
                return render(request, "accounts/login.html", {'form': form})

        return render(request, "accounts/login.html", {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            password_hashed = make_password(form.cleaned_data['password'])
            form.cleaned_data.pop('confirmEmail')
            form.cleaned_data.pop('confirmPassword')
            form.cleaned_data.pop('captcha')
            form.cleaned_data['password'] = password_hashed

            new_user = User(**form.cleaned_data,
                            status=1,
                            is_active=False,
                            # photo=request.FILES['photo'],
                            is2FAEnabled=False,
                            lastLogin=None,
                            lastUpdated=now,
                            dateCreated=now)
            send_email(new_user)
            new_user.save()
            messages.info(request, "Register successful!")
            return render(request, "accounts/register.html", {'form': form})
        else:
            return render(request, "accounts/register.html", {'form': form})


class ActivateView(View):
    def get(self, request):
        form = ActivateForm()
        return render(request, 'accounts/activate.html', {'form': form})

    def post(self, request):
        form = ActivateForm(request.POST)

        if form.is_valid():
            value_email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=value_email)
            except User.DoesNotExist:
                user = None
                messages.error(request, "No user found with the given email address.")

            if user is not None:
                if user.is_active:
                    messages.info(request, "Your account is already activated")
                else:
                    send_email(user)
                    messages.info(request, "Verification mail is sent!")

        return render(request, "accounts/activate.html", {'form': form})

