from django.db import models

from ..models.cidade import Cidade

class Endereco(models.Model):
    id = models.AutoField(primary_key=True)
    endereco_completo = models.CharField(null = True, max_length=500)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'enderecos'