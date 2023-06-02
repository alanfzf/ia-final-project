from django.urls import path
from auth_stuff.views import *

app_name = 'authenticate'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
