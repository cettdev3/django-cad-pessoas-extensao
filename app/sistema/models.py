from django.db import models

# Create your models here.
class Pessoas(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    data_nascimento = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    cpf = models.CharField(max_length=50)
    rg = models.CharField(max_length=50)
    orgao_emissor = models.CharField(max_length=50)
    endereco = models.CharField(max_length=50)
    cep = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    banco = models.CharField(max_length=50)
    agencia = models.CharField(max_length=50)
    conta = models.CharField(max_length=50)
    pix = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    qtd_contratacoes = models.CharField(max_length=11)
    user_camunda = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'processo_gps_professor'