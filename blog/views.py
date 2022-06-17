from blog.models import BlogPost
from django.shortcuts import render

# Create your views here.
from django.views import View
from panel.views import PanelView


class IndexView(View):
    def get(self, request):
        posts = BlogPost.objects.all()
        context = {'posts': posts}
        return render(request, 'blog/index.html', context)


class PostView(View):
    def get(self, request):
        posts = BlogPost.objects.all()
        context = {'posts': posts}
        return render(request, 'blog/index.html', context)


class AddPostView(PanelView):
    def get(self, request):
        form = DoctorForm()
        context = {"current_page": "add_doctor", "form": form}
        return render(request, 'doctor/add_doctor.html', context)

    def post(self, request):
        form = DoctorForm(request.POST, request.FILES)

        if form.is_valid():
            password_hashed = make_password(form.cleaned_data['password'])
            form.cleaned_data.pop('confirmPassword')
            form.cleaned_data.pop('captcha')
            form.cleaned_data['password'] = password_hashed

            new_doctor = User(**form.cleaned_data,
                              role=Roles.DOCTOR.value,
                              # photo=request.FILES['photo'],
                              lastLogin=None,
                              lastUpdated=now,
                              dateCreated=now)
            new_doctor.save()
            return redirect('panel:doctor:doctors')
        else:
            context = {"current_page": "add_doctor", "form": form}
            return render(request, "doctor/add_doctor.html", context)


