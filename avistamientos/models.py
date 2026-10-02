from django.db import models
from mascotas.models import Mascota


class Avistamiento(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    nombre_persona = models.CharField(max_length=100)
    lugar = models.CharField(max_length=150)
    fecha_avistamiento = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.mascota.nombre} vista en {self.lugar}"
