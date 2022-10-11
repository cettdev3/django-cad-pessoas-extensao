from django.db import models

from ..models.evento import Evento
from ..models.pessoa import Pessoas

class Alocacao(models.Model):
    id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, null=True)
    professor = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True) 
    data_inicio = models.DateField(null = True)
    data_fim = models.DateField(null = True)
    status = models.CharField(null = True, max_length=50)   
    observacao = models.CharField(null = True, max_length=500)   
    class Meta:
        db_table = 'alocacoes'