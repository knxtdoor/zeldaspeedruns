from social_core.backends.open_id_connect import OpenIdConnectAuth


class TwitchOpenIdConnect(OpenIdConnectAuth):
    """
    OpenID Connect authentication backend for Twitch using the modern API

    This implementation is currently needed because Python Social Auth's Twitch backend uses an outdated API that is
    no longer working correctly. Twitch developers recommend using their new API and OpenID Connect instead of OAuth2.

    TODO: Remove this when our PR is accepted and update python-social-auth.
    """
    name = 'twitch'
    USERNAME_KEY = 'preferred_username'
    OIDC_ENDPOINT = 'https://id.twitch.tv/oauth2'
    DEFAULT_SCOPE = ['openid', 'user:read:email']
    TWITCH_CLAIMS = '{"id_token":{"email": null,"email_verified":null,"preferred_username":null,"picture":null}}'

    def auth_params(self, state=None):
        params = super().auth_params(state)
        # Twitch, please fix your non-complaint OIDC implementation.
        params['claims'] = self.TWITCH_CLAIMS
        return params

    def get_user_details(self, response):
        return {
            'username': self.id_token['preferred_username'],
            'email': self.id_token['email'],
            # Twitch does not provide this information
            'fullname': '',
            'first_name': '',
            'last_name': '',
        }

    def auth_html(self):
        pass


def update_identities(backend, user, details, response, *args, **kwargs):
    identity = details['username']

    if backend.name == 'discord':
        # We must further transform this to grab the discriminant, too.
        identity = '{}#{}'.format(response['username'], response['discriminator'])

    user.profile.update_social_identity(backend.name, identity)
    user.profile.save()


def disconnect_identity(backend, user, *args, **kwargs):
    user.profile.remove_social_identity(backend.name)
    user.profile.save()
