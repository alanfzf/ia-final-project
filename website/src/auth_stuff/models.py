from django.db import models
from django.contrib.auth.models import AbstractUser
from data_log.models import Tarjeta

class User(AbstractUser):
    rfid_tag = models.ForeignKey(Tarjeta, on_delete=models.SET_NULL, null=True)
