from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.core.cache import cache

@receiver(user_logged_out)
def clear_cache_on_logout(sender, user, request, **kwargs):
     cache.clear()