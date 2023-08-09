from sistema.services.emailService import SMTPClient
from sistema.models import PropostaProjeto, MembroExecucao
from django.template.loader import render_to_string
import envconfiguration as config

class PropostaSubmetidaEmail:
    def __init__(self, proposta_projeto: PropostaProjeto):
        # "gerente.operacional@cett.org.br", "coordenacao.extensao@cett.org.br",
        self.recipient = ["kaikebsilva62@gmail.com"]
        self.titulo_projeto = proposta_projeto.titulo_projeto
        self.proposta_url = config.BASE_URL+"/show-proposta-projeto/"+str(proposta_projeto.pk)
        self.nome_proponente = MembroExecucao.objects.filter(
            proposta_projeto=proposta_projeto,
            role=MembroExecucao.ROLE_PROPONENTE
        ).first().pessoa.nome

        self.email_service = SMTPClient()

    def get_content(self):
        subject = "Proposta de projeto submetida"
        context = {
            'titulo_projeto': self.titulo_projeto,
            'nome_proponente': self.nome_proponente,
            'proposta_url': self.proposta_url
        }
        html_message = render_to_string('emails/propostasubmetidaemail.html', context)
        return subject, html_message

    def send(self):
        subject, html_message = self.get_content()
        self.email_service.subject = subject
        self.email_service.htmlMessage = html_message
        self.email_service.toAddresses = self.recipient
        return self.email_service.send()
