from django.db import models
from ..models.dpEvento import DpEvento
class Galeria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, max_length=100)
    evento = models.ForeignKey(DpEvento, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'galerias'