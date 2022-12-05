from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.models.pessoa import Pessoas
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import datetime
    
@login_required(login_url='/auth-user/login-user')
def calendario(request):
    return render(request, 'componentes/calendario/calendario.html')