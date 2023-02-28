from datetime import datetime
from django.db import models
from ..models.curso import Curso
from django.contrib.auth.models import User
# Create your models here.
class Pessoas(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(null = True, max_length=50)
    nome = models.CharField(null = True, max_length=50)
    sexo = models.CharField(null = True, max_length=50)
    estado_civil = models.CharField(null = True, max_length=50)
    data_nascimento = models.CharField(null = True, max_length=50)
    telefone = models.CharField(null = True, max_length=50)
    telefone_recado = models.CharField(null = True, max_length=50)
    pis_pasep = models.CharField(null = True, max_length=50)
    cpf = models.CharField(null = True, max_length=50)
    rg = models.CharField(null = True, max_length=50)
    data_emissao = models.DateField(null = True)
    orgao_emissor = models.CharField(null = True, max_length=50)
    nome_mae = models.CharField(null = True, max_length=50)
    nome_pai = models.CharField(null = True, max_length=50)
    cep = models.CharField(null = True, max_length=50)
    cargo = models.CharField(null = True, max_length=50)
    banco = models.CharField(null = True, max_length=50)
    agencia = models.CharField(null = True, max_length=50)
    conta = models.CharField(null = True, max_length=50)
    pix = models.CharField(null = True, max_length=50)
    tipo_conta = models.CharField(null = True, max_length=50)
    tipo = models.CharField(null = True, max_length=50)
    qtd_contratacoes = models.CharField(null = True, max_length=11)
    user_camunda = models.CharField(null = True, max_length=50)
    cidade = models.CharField(null = True, max_length=100) 
    bairro = models.CharField(null = True, max_length=100) 
    rua = models.CharField(null = True, max_length=250) 
    cep = models.CharField(null = True, max_length=100) 
    numero_endereco = models.CharField(null = True, max_length=10) 
    complemento = models.CharField(null = True, max_length=250)
    estado = models.CharField(null = True, max_length=50)
    id_protocolo = models.CharField(null = True, max_length=50)
    cursos = models.ManyToManyField(Curso, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank= True)

    class Meta:
        db_table = 'processo_gps_professor'
    
    @property
    def data_nascimento_formatted(self):
        if not self.data_nascimento:
            return ""
        dateFormt = datetime.strptime(self.data_nascimento, "%Y-%m-%d")
        dateStr = dateFormt.strftime("%d-%m-%Y")
        dateFormatted = datetime.strptime(dateStr, "%d-%m-%Y")
        return dateFormatted