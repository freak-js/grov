# Этот модуль предназначен для логики авторизации через декорацию
# контроллеров функцией проверки наличия у пользователя флага is_staff


from django.core.exceptions import PermissionDenied


def is_staff_checker(view):
    """
    Пропускает только ползователей с флагом is_staff.
    """
    def wrapper(request):
        if not request.user.is_staff:
            raise PermissionDenied

        checked_view = view(request)
        return checked_view
    return wrapper
