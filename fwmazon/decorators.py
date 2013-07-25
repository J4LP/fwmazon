from django.core.exceptions import PermissionDenied

def is_manager(view):
    def f(request, *args, **kwargs):
        if request.user.is_manager:
            return view(request, *args, **kwargs)
        raise PermissionDenied
    return f

def is_contractor(view):
    def f(request, *args, **kwargs):
        if request.user.is_manager or request.user.is_contractor:
            return view(request, *args, **kwargs)
        raise PermissionDenied
    return f