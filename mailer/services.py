from django.core.cache import cache

from config.settings import CACHE_ENABLE
from mailer.models import Letter

# def get_owner_letters_from_cache(owner_id):
#     if not CACHE_ENABLE:
#         return Letter.objects.all().filter(owner_id=owner_id)
#     key = "letter_list"
#     letters = cache.get(key)
#     if letters is None:
#         letters = Letter.objects.all().filter(owner_id=owner_id)
#         cache.set(key, letters)
#     return letters


def get_owner_letters_from_cache(owner_id):
    if not CACHE_ENABLE:
        return Letter.objects.all().filter(owner_id=owner_id)
    key = f"letter_list_{owner_id}"
    letters = cache.get(key)
    if letters is None:
        letters = Letter.objects.all().filter(owner_id=owner_id)
        cache.set(key, letters)
    return letters
