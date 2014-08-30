from django.conf import settings

def context(request, extra={}):
  ctx = {
    'APP_ID': settings.APP_ID,
    'user': request.user,
  }

  return dict(ctx.items() + extra.items())