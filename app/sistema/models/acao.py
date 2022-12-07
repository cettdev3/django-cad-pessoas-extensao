from django.db import models
from ..models.cidade import Cidade

class Acao(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(null = True, max_length=50)   
    process_instance = models.FloatField(null = True)
    variaveis = models.JSONField(null = True)
    status = models.CharField(null = True, max_length=50)
    descricao = models.CharField(null = True, max_length=1000)
    data_inicio = models.DateField(null = True)
    data_fim = models.DateField(null = True)
    bairro = models.CharField(null = True, max_length=100)
    logradouro = models.CharField(null = True, max_length=250)
    cep = models.CharField(null = True, max_length=100)
    complemento = models.CharField(null = True, max_length=250)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'acoes'