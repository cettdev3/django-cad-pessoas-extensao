"""extensao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from sistema.views.avaliacaoApiViews import AvaliacaoApiView, AvaliacaoDetailApiView
from sistema.views.pessoaApiViews import PessoaApiView
from sistema.views.siteViews import home, gerencia_pessoas, cadastrar_pessoas, eliminarPessoa, visualizarPessoa, editarPessoa, edicaoPessoa, registrar,menu_rapido

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",menu_rapido),
    path("gerenciar-pessoas",gerencia_pessoas),
    path("cadastrar-pessoas",cadastrar_pessoas),
    path("eliminarPessoa/<codigo>", eliminarPessoa),
    path("visualizarPessoa/<codigo>", visualizarPessoa),
    path("editarPessoa/<codigo>", editarPessoa),
    path("edicaoPessoa",edicaoPessoa),
    path("registrar",registrar),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path("pessoas", PessoaApiView.as_view()),
    path("avaliacoes", AvaliacaoApiView.as_view()),
    path('avaliacoes/<int:avaliacao_id>/', AvaliacaoDetailApiView.as_view()),

]
