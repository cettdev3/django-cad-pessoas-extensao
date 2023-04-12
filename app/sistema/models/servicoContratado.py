from django.db import models

class ServicoContratado(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(null = True, max_length=100)
    valor = models.FloatField(null = True, max_length=100)
    data_limite = models.DateField(null = True)

    class Meta:
        db_table = 'servicos_contratados'