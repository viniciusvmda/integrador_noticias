from django.db import models

class Caderno(models.Model):
    descricao = models.CharField(max_length=200)

class Materia(models.Model):
    titulo = models.CharField(max_length=90)
    caderno= models.ForeignKey('Caderno', on_delete=models.SET_NULL, related_name="caderno", null=True, blank=True)
    data_importacao = models.DateField(auto_now_add=True)
    publicada = models.BooleanField()

    def __str__(self):
        return str("Título: " + str(self.titulo))