from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import View
# requests
import requests
from datetime import datetime
# models
from data_log.models import Registro, Tarjeta

# Create your views here.
class Dashboard(LoginRequiredMixin, ListView):
    model = Registro
    login_url = reverse_lazy('authenticate:login')
    template_name = 'inicio.html'
    context_object_name = 'registros'

class ReviewData(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'review.html'
    context_object_name = 'registro'
    model = Registro

class CSRFExemptMixin(object):

   @method_decorator(csrf_exempt)
   def dispatch(self, *args, **kwargs):
       return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)

class ReceiveData(CSRFExemptMixin, View):
    def post(self, request):
        tag = request.POST.get('tag')
        face = request.FILES.get('face')
        data = None

        if face is None or tag is None:
            return HttpResponseBadRequest("Bad request, you must specify the rfid tag and face image")

        try:
            url = 'http://192.168.0.100:5000/predict'
            resp = requests.post(url, files={'face': face})
            data = resp.json()
        except:
            return HttpResponseServerError("Server error, could not predict a face!")

        if "error" in data:
            return HttpResponseServerError(data.get('error'))

        person = data.get('predicted_face')
        prob = data.get('probability')
        card = None

        try:
            card = Tarjeta.objects.get(id_tarjeta=tag)
        except Tarjeta.DoesNotExist:
            return HttpResponseServerError("RFID tag is not registered in the database!")

        # Create a new instance of MyModel
        register = Registro(persona_predecida=person, 
                            confianza=prob, captura=face, 
                            tarjeta=card)
        register.save()

        return JsonResponse(data)
