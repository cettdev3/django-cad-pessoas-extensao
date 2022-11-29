from django.db import models

class Turno(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, max_length=50)   
    carga_horaria = models.FloatField(null = True)

    class Meta:
        db_table = 'turno'