from django.db import models
from ..models.dpEvento import DpEvento
from ..models.membroExecucao import MembroExecucao
class ServicoContratado(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(null = True, max_length=100)
    valor = models.FloatField(null = True, max_length=100)
    data_limite = models.DateField(null = True)
    evento = models.ForeignKey(DpEvento, on_delete=models.SET_NULL, null = True)
    responsavel = models.ForeignKey(MembroExecucao, on_delete=models.SET_NULL, null = True)
    class Meta:
        db_table = 'servicos_contratados'