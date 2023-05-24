from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.views.generic import RedirectView


class LoginFormView(LoginView):
    template_name = 'start.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('attendance:index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LogoutView(RedirectView):
    pattern_name = 'att_auth:login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
