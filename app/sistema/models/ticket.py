from django.db import models
from ..models.membroExecucao import MembroExecucao
from ..models.cidade import Cidade

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(null = True, max_length=100)
    status = models.CharField(null = True, max_length=100)
    id_protocolo = models.CharField(null = True, max_length=100)
    membro_execucao =  models.ForeignKey(MembroExecucao, on_delete=models.SET_NULL, null=True)
    meta = models.JSONField(null = True)
    data_inicio = models.DateField(null = True, blank= True)
    data_fim = models.DateField(null = True, blank= True)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)

    class Meta:
        db_table = 'tickets'