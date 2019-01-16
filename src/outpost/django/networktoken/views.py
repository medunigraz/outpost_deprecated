from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import (
    DateTimeField,
    ExpressionWrapper,
    F,
)
from django.urls import reverse_lazy as reverse
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
)

from . import (
    forms,
    models,
)


class TokenCreateView(LoginRequiredMixin, CreateView):
    model = models.Token
    form_class = forms.TokenForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('networktoken:detail', kwargs={'pk': self.object.pk})


class TokenDetailView(LoginRequiredMixin, DetailView):
    model = models.Token

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            user=self.request.user
        ).annotate(
            expired=ExpressionWrapper(
                F('created') + F('lifetime'),
                output_field=DateTimeField()
            )
        ).filter(expired__gt=timezone.now())
