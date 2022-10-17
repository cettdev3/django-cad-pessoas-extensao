from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    print("dentro de loginuser")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            messages.error(request, ("Houve um erro verifique suas credenciais e tente novamente"))
            print("login")
            return render(request, "authenticate/login.html", {})  
    else:
        return render(request, "authenticate/login.html", {})  

def logout_user(request):
    logout(request)
    messages.error(request, ("Você foi desconectado"))
    return redirect("/home")  