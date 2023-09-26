# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.alocacao import Alocacao
from ..models.atividade import Atividade
from ..serializers.membroExecucaoSerializer import MembroExecucaoSerializer
from ..serializers.acaoSerializer import AcaoSerializer
from ..serializers.tipoAtividadeSerializer import TipoAtividadeSerializer
from ..serializers.departamentoSerializer import DepartamentoSerializer
from ..serializers.cidadeSerializer import CidadeSerializer
from ..serializers.dpEventoSerializer import DpEventoSerializer
from ..serializers.anexoSerializer import AnexoSerializer
from ..serializers.servicoSerializer import ServicoSerializer
from ..serializers.atividadeCategoriaSerializer import AtividadeCategoriaSerializer
from ..serializers.galeriaSerializer import GaleriaSerializer
from ..serializers.ticketSerializers.ticketSerializer import TicketSerializer
from ..serializers.alocacaoSerializer import AlocacaoSerializer

class AtividadeSerializer(serializers.ModelSerializer):
    acao = AcaoSerializer(many=False, read_only=True)   
    evento = DpEventoSerializer(many=False, read_only=True)
    tipoAtividade = TipoAtividadeSerializer(many=False, read_only=True)
    responsavel = MembroExecucaoSerializer(many=False, read_only=True)
    departamento = DepartamentoSerializer(many=False, read_only=True)
    cidade = CidadeSerializer(many=False, read_only=True) 
    servico_set = ServicoSerializer(many=True, read_only=True)
    galeria = GaleriaSerializer(many=False, read_only=True)
    ticket_set = TicketSerializer(many=True, read_only=True)
    anexos = AnexoSerializer(many=True, read_only=True)
    atividadeCategorias = AtividadeCategoriaSerializer(many=True, read_only=True)
    atividadeCategorias_ids = serializers.SerializerMethodField()
    alocacoes = AlocacaoSerializer(many=True, read_only=True)
    class Meta:
        model = Atividade
        fields = [
            "id",
            "nome",
            "anexos",
            "descricao",
            "linkDocumentos",
            "status",
            "acao",
            "evento",
            "data_realizacao_inicio",
            "data_realizacao_fim",
            "tipoAtividade",
            "responsavel",
            "departamento",
            "cidade",
            "logradouro",
            "bairro",
            "cep",
            "complemento",
            "galeria",
            "quantidadeCertificacoes",
            "quantidadeMatriculas",
            "quantidadeAtendimentos",
            "quantidadeInscricoes",
            "cargaHoraria",
            "servico_set",
            "id_protocolo",
            "valor",
            "ticket_set",
            "atividade_meta",
            "categoria",
            "categoria_label",
            "categoria_badge",
            "atividadeCategorias",
            "atividadeCategorias_ids",
            "carga_horaria_formatada",
            "horario_inicio",
            "horario_fim",
            "alocacoes"
        ]
        
        depth = 4

    def get_atividadeCategorias_ids(self, obj):
        return [categoria.id for categoria in obj.atividadeCategorias.all()]