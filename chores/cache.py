from django.core.cache import get_cache

cache = get_cache('default')

class CachedObjectBase(object):
  key = None
  timeout = None

  def __init__(self, **kwargs):
    self.key = self.key % kwargs

  def set(self, value):
    cache.set(self.key, value, timeout=self.timeout)

  def get(self):
    return cache.get(self.key)

  def clear(self):
    cache.delete(self.key)

class CachedSMSVerificationCode(CachedObjectBase):
  key = 'sms_verification_code_%(user_id)s'
  timeout = 60 * 5




