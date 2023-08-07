from django.db import models
from sistema.models.galeria import Galeria

class Imagem(models.Model):
    id = models.AutoField(primary_key=True)
    id_alfresco = models.CharField(null = True, max_length=100)
    descricao = models.CharField(null = True, max_length=100)
    galeria = models.ForeignKey(Galeria, on_delete=models.SET_NULL, null=True)
    shared_link = models.CharField(null = True, max_length=500)
    show_on_report = models.BooleanField(default=False)

    class Meta:
        db_table = 'imagens'