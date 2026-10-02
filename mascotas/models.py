from django.db import models


class Mascota(models.Model):
    ESTADOS = [
        ('perdida', 'Perdida'),
        ('encontrada', 'Encontrada'),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='perdida')

    def __str__(self):
        return f"{self.nombre} ({self.estado})"
