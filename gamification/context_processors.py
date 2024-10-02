from .models import TeamEmployee


def team_membership(request):
    is_in_team = False
    if request.user.is_authenticated:
        is_in_team = TeamEmployee.objects.filter(employee=request.user).exists()
    return {"is_in_team": is_in_team}
