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
        ]

        isPkRoute = False
        update_atividade_base_url = reverse('update-atividade', kwargs={'pk': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(update_atividade_base_url)

        remove_atividade_base_url = reverse('remove-atividade', kwargs={'pk': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(remove_atividade_base_url)

        update_membro_equipe_base_url = reverse('update-membro-equipe', kwargs={'pk': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(update_membro_equipe_base_url)

        remove_membro_equipe_base_url = reverse('remove-membro-equipe', kwargs={'pk': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(remove_membro_equipe_base_url)

        update_membro_execucao_api_base_url = reverse('membroExecucaoDetail', kwargs={'membro_execucao_id': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(update_membro_execucao_api_base_url)

        update_item_orcamento_base_url = reverse('update-item-orcamento', kwargs={'pk': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(update_item_orcamento_base_url)

        remove_item_orcamento_base_url = reverse('remove-item-orcamento', kwargs={'pk': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(remove_item_orcamento_base_url)

        update_proposta_projeto_base_url = reverse('update-proposta-projeto', kwargs={'pk': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(update_proposta_projeto_base_url)

        remove_proposta_projeto_base_url = reverse('remove-proposta-projeto', kwargs={'pk': 0})[:-1]
        isPkRoute = isPkRoute or request.path_info.startswith(remove_proposta_projeto_base_url)
        
        if not isPkRoute and request.path_info not in included_urls:
            if request.user.is_authenticated:
                if hasattr(request.user, 'pessoa'):
                    if request.user.pessoa.instituicao == 'escola':
                        return redirect('cotec-projeto-index')
