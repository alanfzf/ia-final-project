from datetime import datetime
from django.db import models


# Create your models here.
class Tarjeta(models.Model):
    id_tarjeta = models.CharField(max_length=255, unique=True, blank=False)
    def __str__(self):
        return self.id_tarjeta

class Registro(models.Model):
    persona_predecida = models.CharField(max_length=255, blank=False)
    confianza = models.DecimalField(default=0.0, max_digits=4, decimal_places=4, verbose_name='Nivel de confianza')
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.SET_NULL, null=True)
    captura = models.ImageField(upload_to="uploads/", null=True, blank=True)
    fecha = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.persona_predecida}, {str(self.tarjeta)}"
