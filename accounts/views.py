from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DeleteView
from oauth2_provider.models import Grant

from accounts.forms import SettingsForm, RegisterForm, ProfileSettingsForm


class RegisterView(SuccessMessageMixin, FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:register')
    success_message = 'Your account was created successfully. ' \
                      'You may now sign in.'

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
            messages.add_message(self.request, messages.INFO,
                                 'Your username was changed successfully.')

        if user.email != email:
            user.email = email
            dirty = True
            messages.add_message(self.request, messages.INFO,
                                 'Your email was changed successfully.')

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
            super(AuthorizedApplicationDeleteView, self).delete(request, *args,
                                                                **kwargs)
        else:
            return HttpResponseForbidden(
                "You are not authorized to do this action.")
