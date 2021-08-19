from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView

from accounts.forms import SettingsForm
from accounts.models import ConfirmationToken


class SettingsView(LoginRequiredMixin, FormView):
    form_class = SettingsForm
    template_name = 'accounts/acm.html'
    success_url = reverse_lazy('accounts:acm')

    def get_initial(self):
        user = self.request.user
        return {
            'username': user.username,
            'email': user.email,
        }

    def form_valid(self, form):
        user = self.request.user
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        dirty = False

        if user.username != username:
            user.username = username
            dirty = True
            messages.add_message(self.request, messages.INFO, 'Your username was changed successfully.')

        if user.email != email:
            token = ConfirmationToken.objects.create_token(email=email, user=user)
            send_mail(
                'Confirm your new email address',
                token.code,
                'hylia@zeldaspeedruns.com',
                [email],
            )
            messages.add_message(self.request, messages.WARNING, 'Check your email for a confirmation message.')

        if dirty:
            user.full_clean()
            user.save()

        return super().form_valid(form)


class ConnectionsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/acm_connections.html'


class EmailChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/acm_email_change_done.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code', None)
        if not code:
            raise ValueError('Code must be set')

        token = get_object_or_404(ConfirmationToken, code__exact=code)

        if not token.is_valid_for_user(request.user):
            return redirect(reverse('accounts:acm'))

        with transaction.atomic():
            request.user.email = token.email
            request.user.save()
            token.is_used = True
            token.save()

        return super().get(request, *args, **kwargs)
