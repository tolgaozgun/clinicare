from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class PanelView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect'


class DashboardView(PanelView):
    def get(self, request):
        context = {'current_page': 'home'}
        return render(request, 'panel/dashboard.html', context)