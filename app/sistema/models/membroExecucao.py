from django.db import models
from ..models.cidade import Cidade
from ..models.pessoa import Pessoas
from ..models.acao import Acao
from ..models.itinerario import Itinerario
class MembroExecucao(models.Model):
    id = models.AutoField(primary_key=True)
    data_inicio = models.DateField(null = True, blank= True)
    data_fim = models.DateField(null = True, blank= True)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    tipo = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True, blank= True)
    acao = models.ForeignKey(Acao, on_delete=models.SET_NULL, null=True, blank= True)
    itinerario = models.ForeignKey(Itinerario, on_delete=models.SET_NULL, null=True, blank= True)
    class Meta:
        db_table = 'membros_execucao'