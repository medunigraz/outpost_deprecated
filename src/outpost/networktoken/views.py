from django.urls import reverse_lazy as reverse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models


class TokenCreateView(LoginRequiredMixin, CreateView):
    model = models.Token
    fields = (
        'lifetime',
    )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('networktoken:detail', kwargs={'pk': self.object.pk})


class TokenDetailView(LoginRequiredMixin, DetailView):
    model = models.Token
    fields = (
        'lifetime',
    )

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
