from .models import CustomUser


def get_role(request):
    user = CustomUser.objects.filter(username=request.user.username)
    role = ""
    if len(user) != 0:
        role = CustomUser.USER_TYPE[int(user[0].role) - 1][1]
    return {'role': role}
