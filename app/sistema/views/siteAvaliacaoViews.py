from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.escolaSerializer import EscolaSerializer
from sistema.models.avaliacao import Avaliacao
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework import status

@login_required(login_url='/auth-user/login-user')
def avaliacoesTable(request):
    avaliacoes = Avaliacao.objects.all()
    return render(request,'avaliacoes/avaliacoes_table.html',{'avaliacoes':avaliacoes})

@login_required(login_url='/auth-user/login-user')
def eliminarAvaliacao(request, id):
    avaliacao = Avaliacao.objects.get(id=id)
    avaliacao.delete()
    messages.success(request, 'Avaliação eliminada com sucesso!')
    return JsonResponse({"message": "Deletado com sucesso"}, status=status.HTTP_200_OK)
