from django.db import models
from ..models.atividade import Atividade

class Servico(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, max_length=100)
    descricao = models.CharField(null = True, max_length=1000)
    quantidadeAtendimentos = models.IntegerField(null = True, blank=True)
    quantidadeVendas = models.IntegerField(null = True, blank=True)
    atividade = models.ForeignKey(Atividade, on_delete=models.SET_NULL, null=True, blank=True)
    cidade = models.ForeignKey('Cidade', on_delete=models.SET_NULL, null=True, blank=True)
    logradouro = models.CharField(null = True, max_length=100)
    bairro = models.CharField(null = True, max_length=100)
    cep = models.CharField(null = True, max_length=100)
    complemento = models.CharField(null = True, max_length=100)
    status = models.CharField(null = True, max_length=100)
    class Meta:
        db_table = 'servicos'