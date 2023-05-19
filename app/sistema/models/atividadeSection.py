from django.db import models
from .dpEvento import DpEvento

class AtividadeSection(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, blank=True, max_length=100)
    order = models.IntegerField(null = True, blank=True)
    evento = models.ForeignKey(DpEvento, on_delete=models.SET_NULL, null=True, blank= True)
    
    class Meta:
        db_table = 'secoes_atividades'
   