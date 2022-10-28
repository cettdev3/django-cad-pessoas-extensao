# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..serializers.avaliacaoSerializer import AvaliacaoSerializer
from ..models.avaliacao import Avaliacao
from ..serializers.pessoaSerializer import PessoaSerializer

class AvaliacaoApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny]

    # 1. List all
    def get(self, request, *args, **kwargs):
        cidade = request.GET.get('cidade')
        todos = None
        if cidade:
            todos = Avaliacao.objects.filter(cidade=cidade).all()
        else: 
            todos = Avaliacao.objects.all()
        print("dados em avaliacoes",todos)
        serializer = AvaliacaoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "nome": request.data.get("nome"),
            "endereco": request.data.get("endereco"),
            "curso": request.data.get("curso"),
            "qtd_salas": request.data.get("qtd_salas"),
            "capacidade": request.data.get("capacidade"),
            "qtd_cadeiras": request.data.get("qtd_cadeiras"),
            "qtd_tomadas": request.data.get("qtd_tomadas"),
            "qtd_janelas": request.data.get("qtd_janelas"),
            "tipo_climatizacao": request.data.get("tipo_climatizacao"),
            "qualidade_iluminacao": request.data.get("qualidade_iluminacao"),
            "turnos_disponiveis": request.data.get("turnos_disponiveis"),
            "qtd_banheiros_masculino": request.data.get("qtd_banheiros_masculino"),
            "qtd_banheiros_feminino": request.data.get("qtd_banheiros_feminino"),
            "rede_eletrica": request.data.get("rede_eletrica"),
            "qualidade_bebedouro": request.data.get("qualidade_bebedouro"),
            "acessibilidade": request.data.get("acessibilidade"),
            "internet": request.data.get("internet"),
            "data_show": request.data.get("data_show"),
            "limpeza": request.data.get("limpeza"),
            "link_imagens": request.data.get("link_imagens"),
            "parecer": request.data.get("parecer"),
            "obs_parecer": request.data.get("obs_parecer"),
            "possui_cozinha": request.data.get("possui_cozinha"),
            "capacidade_cozinha": request.data.get("capacidade_cozinha"),
            "qtd_tomadas_cozinha": request.data.get("qtd_tomadas_cozinha"),
            "funcionalidade_fogao": request.data.get("funcionalidade_fogao"),
            "refrigeracao": request.data.get("refrigeracao"),
            "gas": request.data.get("gas"),
            "bancadas_mesas": request.data.get("bancadas_mesas"),
            "capacidade_fornos": request.data.get("capacidade_fornos"),
            "qtd_fornos": request.data.get("qtd_fornos"),
            "ventilacao_cozinha": request.data.get("ventilacao_cozinha"),
            "torneiras_funcionam": request.data.get("torneiras_funcionam"),
            "area_complementar": request.data.get("area_complementar"),
            "observacao_cozinha": request.data.get("observacao_cozinha"),
            "laboratorio_informatica": request.data.get("laboratorio_informatica"),
            "qtd_computadores": request.data.get("qtd_computadores"),
            "cabeamento_internet": request.data.get("cabeamento_internet"),
            "qtd_computadores_wifi": request.data.get("qtd_computadores_wifi"),
            "obs_informatica": request.data.get("obs_informatica"),
            "lavatorio": request.data.get("lavatorio"),
            "qtd_lavatorio_sb": request.data.get("qtd_lavatorio_sb"),
            "cadeiras_de_sb": request.data.get("cadeiras_de_sb"),
            "qtd_cadeiras_sb": request.data.get("qtd_cadeiras_sb"),
            "cidade": request.data.get("cidade"),
            "obsinfra": request.data.get("obsinfra"),
            "cidade_realizacao": request.data.get("cidade_realizacao"),
            "avalLocalEmailAvaliador": request.data.get("avalLocalEmailAvaliador"),
            "tipoAvaliacao": request.data.get("tipoAvaliacao"),
            "endereco_realizacao": request.data.get("endereco_realizacao"),
            "observacao_beleza": request.data.get("observacao_beleza"),
            "sevicodebeleza": request.data.get("sevicodebeleza"),
            "confeitaria": request.data.get("confeitaria"),
            "UsuariolAvaliador": request.data.get("UsuariolAvaliador"),
            "avalLocalNomeAvaliador": request.data.get("avalLocalNomeAvaliador"),
            "infomatica": request.data.get("infomatica"),
        }

        serializer = AvaliacaoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AvaliacaoDetailApiView(APIView):
    def get_object(self, avaliacao_id):
        try:
            return Avaliacao.objects.get(id=avaliacao_id)
        except Avaliacao.DoesNotExist:
            return None
            
    # 3. Retrieve
    def get(self, request, avaliacao_id, *args, **kwargs):

        avaliacao = self.get_object(avaliacao_id)
        if not avaliacao:
            return Response(
                {"res": "Não existe avaliação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AvaliacaoSerializer(avaliacao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, avaliacao_id, *args, **kwargs):

        avaliacao = self.get_object(avaliacao_id)
        if not avaliacao:
            return Response(
                {"res": "Não existe avaliação com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        if request.data.get("nome"):
            data["nome"] = request.data.get("nome")
        if request.data.get("endereco"):
            data["endereco"] = request.data.get("endereco")
        if request.data.get("curso"):
            data["curso"] = request.data.get("curso")
        if request.data.get("qtd_salas"):
            data["qtd_salas"] = request.data.get("qtd_salas")
        if request.data.get("capacidade"):
            data["capacidade"] = request.data.get("capacidade")
        if request.data.get("qtd_cadeiras"):
            data["qtd_cadeiras"] = request.data.get("qtd_cadeiras")
        if request.data.get("qtd_tomadas"):
            data["qtd_tomadas"] = request.data.get("qtd_tomadas")
        if request.data.get("qtd_janelas"):
            data["qtd_janelas"] = request.data.get("qtd_janelas")
        if request.data.get("tipo_climatizacao"):
            data["tipo_climatizacao"] = request.data.get("tipo_climatizacao")
        if request.data.get("qualidade_iluminacao"):
            data["qualidade_iluminacao"] = request.data.get("qualidade_iluminacao")
        if request.data.get("turnos_disponiveis"):
            data["turnos_disponiveis"] = request.data.get("turnos_disponiveis")
        if request.data.get("qtd_banheiros_masculino"):
            data["qtd_banheiros_masculino"] = request.data.get("qtd_banheiros_masculino")
        if request.data.get("qtd_banheiros_feminino"):
            data["qtd_banheiros_feminino"] = request.data.get("qtd_banheiros_feminino")
        if request.data.get("rede_eletrica"):
            data["rede_eletrica"] = request.data.get("rede_eletrica")
        if request.data.get("qualidade_bebedouro"):
            data["qualidade_bebedouro"] = request.data.get("qualidade_bebedouro")
        if request.data.get("acessibilidade"):
            data["acessibilidade"] = request.data.get("acessibilidade")
        if request.data.get("internet"):
            data["internet"] = request.data.get("internet")
        if request.data.get("data_show"):
            data["data_show"] = request.data.get("data_show")
        if request.data.get("limpeza"):
            data["limpeza"] = request.data.get("limpeza")
        if request.data.get("link_imagens"):
            data["link_imagens"] = request.data.get("link_imagens")
        if request.data.get("parecer"):
            data["parecer"] = request.data.get("parecer")
        if request.data.get("obs_parecer"):
            data["obs_parecer"] = request.data.get("obs_parecer")
        if request.data.get("possui_cozinha"):
            data["possui_cozinha"] = request.data.get("possui_cozinha")
        if request.data.get("capacidade_cozinha"):
            data["capacidade_cozinha"] = request.data.get("capacidade_cozinha")
        if request.data.get("qtd_tomadas_cozinha"):
            data["qtd_tomadas_cozinha"] = request.data.get("qtd_tomadas_cozinha")
        if request.data.get("funcionalidade_fogao"):
            data["funcionalidade_fogao"] = request.data.get("funcionalidade_fogao")
        if request.data.get("refrigeracao"):
            data["refrigeracao"] = request.data.get("refrigeracao")
        if request.data.get("gas"):
            data["gas"] = request.data.get("gas")
        if request.data.get("bancadas_mesas"):
            data["bancadas_mesas"] = request.data.get("bancadas_mesas")
        if request.data.get("capacidade_fornos"):
            data["capacidade_fornos"] = request.data.get("capacidade_fornos")
        if request.data.get("qtd_fornos"):
            data["qtd_fornos"] = request.data.get("qtd_fornos")
        if request.data.get("ventilacao_cozinha"):
            data["ventilacao_cozinha"] = request.data.get("ventilacao_cozinha")
        if request.data.get("torneiras_funcionam"):
            data["torneiras_funcionam"] = request.data.get("torneiras_funcionam")
        if request.data.get("area_complementar"):
            data["area_complementar"] = request.data.get("area_complementar")
        if request.data.get("observacao_cozinha"):
            data["observacao_cozinha"] = request.data.get("observacao_cozinha")
        if request.data.get("laboratorio_informatica"):
            data["laboratorio_informatica"] = request.data.get("laboratorio_informatica")
        if request.data.get("qtd_computadores"):
            data["qtd_computadores"] = request.data.get("qtd_computadores")
        if request.data.get("cabeamento_internet"):
            data["cabeamento_internet"] = request.data.get("cabeamento_internet")
        if request.data.get("qtd_computadores_wifi"):
            data["qtd_computadores_wifi"] = request.data.get("qtd_computadores_wifi")
        if request.data.get("obs_informatica"):
            data["obs_informatica"] = request.data.get("obs_informatica")
        if request.data.get("lavatorio"):
            data["lavatorio"] = request.data.get("lavatorio")
        if request.data.get("qtd_lavatorio_sb"):
            data["qtd_lavatorio_sb"] = request.data.get("qtd_lavatorio_sb")
        if request.data.get("cadeiras_de_sb"):
            data["cadeiras_de_sb"] = request.data.get("cadeiras_de_sb")
        if request.data.get("qtd_cadeiras_sb"):
            data["qtd_cadeiras_sb"] = request.data.get("qtd_cadeiras_sb")
        if request.data.get("cidade"):
            data["cidade"] = request.data.get("cidade")
        if request.data.get("obsinfra"):
            data["obsinfra"] = request.data.get("obsinfra")
        if request.data.get("cidade_realizacao"):
            data["cidade_realizacao"] = request.data.get("cidade_realizacao")
        if request.data.get("avalLocalEmailAvaliador"):
            data["avalLocalEmailAvaliador"] = request.data.get("avalLocalEmailAvaliador")
        if request.data.get("tipoAvaliacao"):
            data["tipoAvaliacao"] = request.data.get("tipoAvaliacao")
        if request.data.get("endereco_realizacao"):
            data["endereco_realizacao"] = request.data.get("endereco_realizacao")
        if request.data.get("observacao_beleza"):
            data["observacao_beleza"] = request.data.get("observacao_beleza")
        if request.data.get("sevicodebeleza"):
            data["sevicodebeleza"] = request.data.get("sevicodebeleza")
        if request.data.get("confeitaria"):
            data["confeitaria"] = request.data.get("confeitaria")
        if request.data.get("UsuariolAvaliador"):
            data["UsuariolAvaliador"] = request.data.get("UsuariolAvaliador")
        if request.data.get("avalLocalNomeAvaliador"):
            data["avalLocalNomeAvaliador"] = request.data.get("avalLocalNomeAvaliador")
        if request.data.get("infomatica"):
            data["infomatica"] = request.data.get("infomatica")

        serializer = AvaliacaoSerializer(instance = avaliacao, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 5. Delete
    def delete(self, request, avaliacao_id, *args, **kwargs):
        
        avaliacao = self.get_object(avaliacao_id)
        if not avaliacao:
            return Response(
                {"res": "Não existe avaliação com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        avaliacao.delete()
        return Response(
            {"res": "Avaliação deletada!"},
            status=status.HTTP_200_OK
        )
