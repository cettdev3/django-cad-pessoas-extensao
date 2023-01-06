from django.db import models
from ..models.cidade import Cidade
from ..models.escola import Escola
from ..models.pessoa import Pessoas

class Itinerario(models.Model):
    id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = 'itinerario'