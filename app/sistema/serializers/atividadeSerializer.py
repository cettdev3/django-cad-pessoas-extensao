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
from ..serializers.servicoSerializer import ServicoSerializer

class AtividadeSerializer(serializers.ModelSerializer):
    acao = AcaoSerializer(many=False, read_only=True)   
    evento = DpEventoSerializer(many=False, read_only=True)
    tipoAtividade = TipoAtividadeSerializer(many=False, read_only=True)
    responsavel = MembroExecucaoSerializer(many=False, read_only=True)
    departamento = DepartamentoSerializer(many=False, read_only=True)
    cidade = CidadeSerializer(many=False, read_only=True) 
    servico_set = ServicoSerializer(many=True, read_only=True)
    class Meta:
        model = Atividade
        fields = [
            "id",
            "descricao",
            "linkDocumentos",
            "status",
            "acao",
            "evento",
            "tipoAtividade",
            "responsavel",
            "departamento",
            "cidade",
            "logradouro",
            "bairro",
            "cep",
            "complemento",
            "quantidadeCertificacoes",
            "quantidadeMatriculas",
            "quantidadeAtendimentos",
            "quantidadeInscricoes",
            "cargaHoraria",
            "servico_set"
        ]
        depth = 2
