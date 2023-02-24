from django.db import models
from ..models.atividade import Atividade

class Servico(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, max_length=100)
    quantidadeAtendimentos = models.IntegerField(null = True, blank=True)
    quantidadeVendas = models.IntegerField(null = True, blank=True)
    atividade = models.ForeignKey(Atividade, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'servicos'