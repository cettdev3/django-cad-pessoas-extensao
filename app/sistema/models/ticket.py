from django.db import models
from ..models.membroExecucao import MembroExecucao

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(null = True, max_length=100)
    status = models.CharField(null = True, max_length=100)
    id_protocolo = models.CharField(null = True, max_length=100)
    membro_execucao =  models.OneToOneField(MembroExecucao, on_delete=models.SET_NULL, null=True)
    meta = models.JSONField(null = True)

    class Meta:
        db_table = 'tickets'