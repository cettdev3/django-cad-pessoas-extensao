from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from sistema.models import Pessoas

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.pessoa.instituicao == Pessoas.INSTITUICAO_CETT:
                return redirect("/home")
            else:   
                return redirect("/cotec-projeto-index")
        else:
            messages.error(request, ("Houve um erro verifique suas credenciais e tente novamente"))
            return render(request, "authenticate/login.html", {})  
    else:
        return render(request, "authenticate/login.html", {})  

def logout_user(request):
    logout(request)
    return redirect("/home")  