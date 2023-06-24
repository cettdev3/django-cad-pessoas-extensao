from django.db import models
from ..models.endereco import Endereco
from ..models.cidade import Cidade

class Escola(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, max_length=100)
    bairro = models.CharField(null = True, max_length=100) 
    logradouro = models.CharField(null = True, max_length=250) 
    cep = models.CharField(null = True, max_length=100) 
    complemento = models.CharField(null = True, max_length=250)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
    id_siga = models.IntegerField(null = True)

    class Meta:
        db_table = 'escolas'