# Этот модуль предназначен для логики авторизации через декорацию
# контроллеров функцией проверки наличия токена в запросе


from django.core.exceptions import PermissionDenied

from hvoya.settings import AUTH_TOKEN


def token_checker(view):
    def wrapper(request):
        token = request.GET.get('token')

        if not token or token != AUTH_TOKEN:
            raise PermissionDenied

        checked_view = view(request)
        return checked_view
    return wrapper