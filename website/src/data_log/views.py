from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'inicio.html'
