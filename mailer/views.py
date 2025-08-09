from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from mailer.models import Letter
from mailer.services import get_owner_letters_from_cache


class LetterListView(LoginRequiredMixin, ListView):
    model = Letter

    def get_queryset(self):
        owner_id = self.request.user.id  # Получение id текущего пользователя
        return get_owner_letters_from_cache(owner_id)
