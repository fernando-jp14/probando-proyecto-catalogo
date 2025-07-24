from django.db import models

class Curso(models.Model):
    DIFICULTAD_OPCIONES = [
        ('Básico', 'Básico'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]

    curso = models.CharField(max_length=100)
    duracion = models.CharField(max_length=50, blank=True)        # ← Ahora permite validación por formulario
    plataforma = models.CharField(max_length=100, blank=True)     # ← Igual aquí
    dificultad = models.CharField(max_length=50, choices=DIFICULTAD_OPCIONES)

    def __str__(self):
        return self.curso