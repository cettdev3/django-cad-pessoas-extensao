from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.userSerializer import UserSerializer
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def usersSelect(request):
    users = User.objects.all()
    return render(request,'users/users_select.html',{'users':users})
