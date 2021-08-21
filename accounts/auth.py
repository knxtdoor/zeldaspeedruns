from social_core.backends.open_id_connect import OpenIdConnectAuth


class TwitchOpenIdConnect(OpenIdConnectAuth):
    """
    OpenID Connect authentication backend for Twitch using the modern API

    This implementation is currently needed because Python Social Auth's Twitch backend uses an outdated API that is
    no longer working correctly. Twitch developers recommend using their new API and OpenID Connect instead of OAuth2.

    TODO: Remove this when our PR is accepted and update python-social-auth.
    """
    name = 'twitch'
    OIDC_ENDPOINT = 'https://id.twitch.tv/oauth2'
    DEFAULT_SCOPE = ['openid', 'user:read:email']

    def auth_params(self, state=None):
        params = super().auth_params(state)
        # Twitch, please fix your non-complaint OIDC implementation.
        params['claims'] = '{"id_token":{"email": null,"email_verified":null},"userinfo":{"picture": null}}'
        return params
    
    def get_user_details(self, response):
        return super(TwitchOpenIdConnect, self).get_user_details(response)

    def auth_html(self):
        pass
