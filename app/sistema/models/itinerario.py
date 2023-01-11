from django.db import models
from ..models.cidade import Cidade
from ..models.escola import Escola
from ..models.pessoa import Pessoas

class Itinerario(models.Model):
    id = models.AutoField(primary_key=True)
    color = models.CharField(null = True, max_length=20, blank= True)
    
    class Meta:
        db_table = 'itinerarios'