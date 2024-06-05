from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            role = CustomUser.objects.get(username=request.user.username).role
            if role:
                role = CustomUser.USER_TYPE[int(role) - 1][1]
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func

    return decorator
