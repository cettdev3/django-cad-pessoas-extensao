from django.db import models
from ..models.cidade import Cidade

class Acao(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(null = True, blank= True, max_length=50)   
    process_instance = models.CharField(null = True, blank= True, max_length=300)
    variaveis = models.JSONField(null = True, blank= True)
    status = models.CharField(null = True, max_length=50, blank= True)
    descricao = models.CharField(null = True, max_length=1000, blank= True)
    data_inicio = models.DateField(null = True, blank= True)
    data_fim = models.DateField(null = True, blank= True)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)

    class Meta:
        db_table = 'acoes'