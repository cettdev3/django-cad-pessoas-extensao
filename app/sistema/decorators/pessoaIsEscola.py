from functools import wraps
from django.shortcuts import redirect

def pessoa_is_escola(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'pessoa'):
            if request.user.pessoa.instituicao == 'escola':
                return redirect('cotec-projeto-index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
