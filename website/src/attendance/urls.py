from django.urls import path
from attendance.views import *

app_name = 'attendance'

urlpatterns = [
    path('', AboutView.as_view(), name='index'),
    path('users/', UsersView.as_view(), name='users'),
    path('card/', RFIDView.as_view(), name='card')
]
