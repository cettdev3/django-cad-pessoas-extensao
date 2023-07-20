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
        ]

        if request.path_info not in included_urls:
            if request.user.is_authenticated:
                if hasattr(request.user, 'pessoa'):
                    if request.user.pessoa.instituicao == 'escola':
                        return redirect('cotec-projeto-index')
