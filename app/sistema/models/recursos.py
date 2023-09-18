from django.db import models
from sistema.models import PropostaProjeto

class Recursos(models.Model):
    proposta_projeto = models.ForeignKey(PropostaProjeto, on_delete=models.CASCADE, related_name='recursos', null=True, blank=True)
    nome = models.TextField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    quantidade = models.IntegerField(null=True, blank=True)
    unidade = models.CharField(max_length=255, null=True, blank=True)
    valor = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    evento = models.ForeignKey('DpEvento', on_delete=models.SET_NULL, null=True, blank= True, related_name='recursos')
    em_estoque = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'recursos'
