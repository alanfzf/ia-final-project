from django.urls import path
from data_log.views import *

app_name = 'data'

urlpatterns = [
    path('', Dashboard.as_view(), name='index'),
]
