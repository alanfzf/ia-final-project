from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.list import View

class AboutView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('att_auth:login')
    template_name = "landing.html"

class UsersView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('att_auth:login')
    template_name = "users.html"

class CSRFExemptMixin(object):
   @method_decorator(csrf_exempt)
   def dispatch(self, *args, **kwargs):
       return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)

class RFIDView(CSRFExemptMixin, View):
    def post(self, request):
        my_data = request.POST
        print(my_data)
        return JsonResponse({"status": True})
