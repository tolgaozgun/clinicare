from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.timezone import now
from django.views import View
from panel.models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class LogoutView(View):
    def get(self, request):
        logout(request)
        print("Logout request recieved")
        return redirect('base:index')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'main/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            value_email = form.cleaned_data['email']
            value_password = form.cleaned_data['password']

            try:
                User.objects.get(email=value_email)
            except User.DoesNotExist:
                messages.error(request, "No user found.")

            print("Email " + value_email + " Password: " + value_password)
            user = authenticate(request, email=value_email, password=value_password)

            if user is not None:
                login(request, user)
                print("Login success for user")
                return redirect('base:index')
            else:
                messages.error(request, "Password invalid.")
                print("Login failed")
                return render(request, "main/login.html", {'form': form})
        else:
            return render(request, "main/login.html", {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'main/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        # doctor_form = RegisterDoctorForm(request.POST)

        if form.is_valid():
            password_hashed = make_password(form.cleaned_data['password'])
            new_patient = User(first_name=form.cleaned_data['first_name'],
                               last_name=form.cleaned_data['last_name'],
                               email=form.cleaned_data['email'],
                               phone=form.cleaned_data['phone'],
                               status=1,
                               role=1,
                               photo="profile/avatar.png",
                               password=password_hashed,
                               isActivated=False,
                               is2FAEnabled=False,
                               lastLogin=None,
                               lastUpdated=now,
                               dateCreated=now)
            new_patient.save()
            return redirect("base:index")
        else:
            return render(request, "main/register.html", {'form': form})
