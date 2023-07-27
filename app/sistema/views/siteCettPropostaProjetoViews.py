from django.shortcuts import render, redirect
from sistema.models import Pessoas, Curso, Atividade, Cidade, MembroExecucao, OrcamentoItem, Orcamento
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from sistema.models import PropostaProjeto
from django.db import transaction
import requests
from rest_framework.authtoken.models import Token
from django.contrib import messages

