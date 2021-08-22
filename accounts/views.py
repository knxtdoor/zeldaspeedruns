from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView, ListView, DeleteView
from oauth2_provider.models import Grant

from accounts.forms import SettingsForm, RegisterForm, ProfileSettingsForm
from accounts.models import ConfirmationToken


class RegisterView(SuccessMessageMixin, FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:register')
    success_message = 'Your account was created successfully. You may now sign in.'

    def form_valid(self, form):
        user = get_user_model().objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
        )

        user.set_password(form.cleaned_data['password1'])
        user.save()

        return super(RegisterView, self).form_valid(form)


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


class ProfileSettingsView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ProfileSettingsForm
    template_name = 'accounts/acm_profile.html'
    success_url = reverse_lazy('accounts:manage_profile')
    success_message = 'Your profile has been updated successfully.'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.form_class
        profile = self.request.user.profile
        return form_class(instance=profile, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
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


class AuthorizedApplicationsListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/acm_applications.html'
    model = Grant
    context_object_name = 'authorized_applications'

    def get_queryset(self):
        return Grant.objects.filter(user_id__exact=self.request.user.id)


class AuthorizedApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Grant
    success_url = reverse_lazy('accounts:applications')

    def delete(self, request, *args, **kwargs):
        grant = self.get_object()
        if grant.user == request.user:
            super(AuthorizedApplicationDeleteView, self).delete(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to do this action.")
