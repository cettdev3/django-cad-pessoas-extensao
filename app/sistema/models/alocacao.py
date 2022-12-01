from django.db import models
import datetime
from ..models.evento import Evento
from ..models.cidade import Cidade
from ..models.pessoa import Pessoas
from ..models.curso import Curso
from ..models.turno import Turno

class Alocacao(models.Model):
    id = models.AutoField(primary_key=True)
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, null=True)
    professor = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True) 
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True) 
    data_inicio = models.DateField(null = True)
    data_fim = models.DateField(null = True)
    status = models.CharField(null = True, max_length=50)   
    observacao = models.CharField(null = True, max_length=500)
    bairro = models.CharField(null = True, max_length=100) 
    logradouro = models.CharField(null = True, max_length=250) 
    cep = models.CharField(null = True, max_length=100) 
    complemento = models.CharField(null = True, max_length=250)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
    turnos = models.ManyToManyField(Turno, blank=True)
    aulas_sabado = models.BooleanField(default=False)
    class Meta:
        db_table = 'alocacoes'
    