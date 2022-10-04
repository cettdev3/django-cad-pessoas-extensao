from django.db import models

class Endereco(models.Model):
    id = models.AutoField(primary_key=True)
    endereco_completo = models.CharField(null = True, max_length=500)
    class Meta:
        db_table = 'enderecos'