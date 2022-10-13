from django.db import models
from ..models.endereco import Endereco

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    data_inicio = models.DateTimeField(null = True)
    data_fim = models.DateTimeField(null = True)
    observacao = models.CharField(null = True, max_length=500)
    status = models.CharField(null = True, max_length=100)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'eventos'