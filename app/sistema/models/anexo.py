from django.db import models

class Anexo(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, blank=True, max_length=1000)
    fonte = models.CharField(null = True, blank=True, max_length=100)
    descricao = models.CharField(null = True, blank=True, max_length=300)
    mime_type = models.CharField(null = True, blank=True, max_length=100)
    model = models.CharField(null = True, blank=True, max_length=100)
    id_model = models.IntegerField(null = True, blank=True)
    id_alfresco = models.CharField(null = True, max_length=100)
    shared_link = models.CharField(null = True, max_length=500)

    class Meta:
        db_table = 'anexos'

    @property
    def extension(self):
        if self.nome:
            ext = self.nome.split('.')[-1]
            if ext in ['pdf']:
                return "pdf"
            elif ext in ['doc', 'docx']:
                return "doc"
            elif ext in ['xls', 'xlsx']:
                return "xls"
            elif ext in ['ppt', 'pptx']:
                return "ppt"
            elif ext in ['jpg', 'jpeg', 'png', 'gif', "webp"]:
                return "img"
            else:
                return "file"