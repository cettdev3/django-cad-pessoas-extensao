from django.db import models

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, max_length=100)

    class Meta:
        db_table = 'departamentos'