from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

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
        user.username = form.data['username']
        user.email = form.data['email']

        if form.data['avatar'] or 'avatar-clear' in form.data:
            user.avatar = form.data['avatar']

        user.save()
        return super().form_valid(form)
