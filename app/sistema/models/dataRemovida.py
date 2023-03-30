from django.db import models
from .alocacao import Alocacao

class DataRemovida(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null = True)
    alocacao = models.ForeignKey(Alocacao, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'datas_removidas'

    @property
    def date_formatted(self):
        return self.date.strftime('%d/%m/%Y')