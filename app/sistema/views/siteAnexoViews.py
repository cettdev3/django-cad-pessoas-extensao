from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import json
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def saveAnexo(request):
    payload = json.loads(request.body)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/anexos'
    body = payload
    response = requests.post(url, json=body, headers=headers)

    anexo = json.loads(response.content)
    return render(
        request,
        'anexos/anexo-card.html',
        {
            'anexo': anexo
        }
    )


@login_required(login_url='/auth-user/login-user')
def deleteAnexo(request, anexo_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/anexos/' + str(anexo_id)
    response = requests.delete(url, headers=headers)
    return JsonResponse({'status': response.status_code, 'message': response.content.decode()})


