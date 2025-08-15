from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from mailer.forms import LetterForm, RecipientForm
from mailer.models import Letter, Recipient
from mailer.services import get_owner_letters_from_cache


class LetterListView(LoginRequiredMixin, ListView):
    model = Letter
    paginate_by = 5  # Количество объектов - писем на странице

    def get_queryset(self):
        owner_id = self.request.user.id  # Получение id текущего пользователя
        return get_owner_letters_from_cache(owner_id)


class LetterDetailView(LoginRequiredMixin, DetailView):
    model = Letter


class LetterCreateView(LoginRequiredMixin, CreateView):
    model = Letter
    form_class = LetterForm

    def get_success_url(self):
        return reverse_lazy('mailer:letter_list', kwargs={'pk': self.request.user.pk})

    # Чтобы автоматически установить текущего пользователя как владельца
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LetterUpdateView(LoginRequiredMixin, UpdateView):
    model = Letter
    form_class = LetterForm

    def get_success_url(self):
        return reverse_lazy('mailer:letter_list', kwargs={'pk': self.request.user.pk})


class LetterDeleteView(LoginRequiredMixin, DeleteView):
    model = Letter

    def get_success_url(self):
        return reverse_lazy('mailer:letter_list', kwargs={'pk': self.request.user.pk})


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    paginate_by = 5  # Количество объектов - адресатов на странице

    def get_queryset(self):
        owner_id = self.request.user.id  # Получение id текущего пользователя
        queryset = super().get_queryset()
        return queryset.filter(owner=owner_id)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy('mailer:recipient_list', kwargs={'pk': self.request.user.pk})

    # Чтобы автоматически установить текущего пользователя как владельца
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy('mailer:recipient_list', kwargs={'pk': self.request.user.pk})


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient

    def get_success_url(self):
        return reverse_lazy('mailer:recipient_list', kwargs={'pk': self.request.user.pk})
