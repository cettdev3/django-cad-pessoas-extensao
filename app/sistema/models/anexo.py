from django.db import models

class Anexo(models.Model):
    ANEXO_TIPO_RELATORIO_PROFESSOR = 'relatorio_professor'
    ANEXO_TIPO_LISTA_PRESENCA = 'lista_presenca'
    ANEXO_TIPO_OUTRO = 'outro'

    ANEXO_TIPO_CHOICES = (
        (ANEXO_TIPO_RELATORIO_PROFESSOR, 'Relatório do(a) professor(a)'),
        (ANEXO_TIPO_LISTA_PRESENCA, 'Lista de presença'),
        (ANEXO_TIPO_OUTRO, 'Outro'),
    )

    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, blank=True, max_length=1000)
    fonte = models.CharField(null = True, blank=True, max_length=100)
    descricao = models.CharField(null = True, blank=True, max_length=300)
    mime_type = models.CharField(null = True, blank=True, max_length=100)
    model = models.CharField(null = True, blank=True, max_length=100)
    id_model = models.IntegerField(null = True, blank=True)
    id_alfresco = models.CharField(null = True, max_length=100)
    shared_link = models.CharField(null = True, max_length=500)
    tipo = models.CharField(null = True, max_length=100)

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

    @property
    def tipo_anexo_formatado(self):
        if not self.tipo:
            return ""
        if self.tipo == self.ANEXO_TIPO_RELATORIO_PROFESSOR:
            return "Relatório do(a) professor(a)"
        elif self.tipo == self.ANEXO_TIPO_LISTA_PRESENCA:
            return "Lista de presença"
        elif self.tipo == self.ANEXO_TIPO_OUTRO:
            return "Outro"