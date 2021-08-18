from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from accounts.forms import SettingsForm


class SettingsView(LoginRequiredMixin, FormView):
    template_name = 'accounts/acm.html'
    form_class = SettingsForm
    success_url = reverse_lazy('accounts:acm')

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.user.username
        initial['email'] = self.request.user.email
        initial['avatar'] = self.request.user.avatar
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']

        if form.clean()['avatar'] or 'avatar-clear' in form.cleaned_data:
            user.avatar = form.cleaned_data['avatar']

        user.save()
        return super().form_valid(form)


class ConnectionsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/acm_connections.html'
