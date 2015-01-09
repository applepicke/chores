from django.conf import settings

def context(request, extra={}):
  ctx = {
    'APP_ID': settings.APP_ID,
    'user': request.user,
    'app_user': request.app_user,
    'house': request.app_user.house if request.app_user else None,
  }

  return dict(ctx.items() + extra.items())