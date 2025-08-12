from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from mailer.forms import LetterForm
from mailer.models import Letter
from mailer.services import get_owner_letters_from_cache


class LetterListView(LoginRequiredMixin, ListView):
    model = Letter

    def get_queryset(self):
        owner_id = self.request.user.id  # Получение id текущего пользователя
        return get_owner_letters_from_cache(owner_id)


class LetterCreateView(LoginRequiredMixin, CreateView):
    model = Letter
    form_class = LetterForm

    def get_success_url(self):
        return reverse_lazy('mailer:letter_list', kwargs={'pk': self.request.user.pk})

    # Чтобы автоматически установить текущего пользователя как владельца
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LetterDeleteView(LoginRequiredMixin, DeleteView):
    model = Letter

    def get_success_url(self):
        return reverse_lazy('mailer:letter_list', kwargs={'pk': self.request.user.pk})
