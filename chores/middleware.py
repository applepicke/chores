
class UserMiddleware(object):
  def process_request(self, request):

    if not request.user:
      pass

    return request

  def process_response(self, request, response):

    return response