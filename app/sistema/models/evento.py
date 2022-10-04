from django.db import models
from app.sistema.models.endereco import Endereco

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    data_inicio = models.DateField(null = True)
    data_fim = models.DateField(null = True)
    observacao = models.CharField(null = True, max_length=500)
    cidade = models.CharField(null = True, max_length=50)
    enderecos = models.ManyToManyField(Endereco, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'eventos'