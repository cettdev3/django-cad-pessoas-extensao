from django.shortcuts import redirect
from django.urls import reverse

class InstituicaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        included_urls = [
            reverse('cotec-projeto-index'),
            reverse('cotec-projeto-form'),
            reverse('auth-user-login'),
            reverse('auth-user-logout'),
            reverse('confirm-delete-modal'),
            reverse('pessoa-modal'),
            reverse('cursos-select'),
            reverse('pessoa-create'),
            reverse('select-multiple-component'),
            reverse('create-proposta-projeto'),
            reverse('proposta-projeto-table'),
            reverse('create-atividade'),
            reverse('create-membro-equipe'),
            reverse('membroExecucao'),
            reverse('create-item-orcamento'),
            reverse('cotec-projeto-success'),
            reverse('membro-execucao-roles'),
            reverse('membros-execucao-all'),
            reverse('form-alocacao-membro-equipe'),
            reverse('save-alocacao'),
            reverse('status-proposta-menu'),
        ]

        dynamic_urls = [
            'update-atividade',
            'remove-atividade',
            'update-membro-equipe',
            'remove-membro-equipe',
            'membroExecucaoDetail',
            'update-item-orcamento',
            'remove-item-orcamento',
            'update-proposta-projeto',
            'remove-proposta-projeto',
            'eliminar-alocacao',
            'editar-alocacao',
            'get-membro-execucao',
            'get-atividade',
            'proposta-projeto-view'
        ]
        
        isPkRoute = False
        for url_name in dynamic_urls:
            base_url = reverse(url_name, kwargs={'id': 0} if 'id' in url_name else {'pk': 0})[:-1]
            stripped_base_url = base_url[:-1]
            stripped_path_info = request.path_info[:-2]
            if stripped_path_info == stripped_base_url:
                isPkRoute = True
                break

        
        if request.user.is_authenticated:
            if hasattr(request.user, 'pessoa'):
                if request.user.pessoa.instituicao == 'escola':
                    if not (isPkRoute or request.path_info in included_urls):
                        return redirect('cotec-projeto-index')
