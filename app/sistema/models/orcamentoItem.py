from django.db import models
from sistema.models import Orcamento

class OrcamentoItem(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=255, null=True, blank=True)
    quantidade = models.IntegerField(null=True, blank=True)
    unidade = models.CharField(max_length=255, null=True, blank=True)
    valor = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'orcamento_itens'
