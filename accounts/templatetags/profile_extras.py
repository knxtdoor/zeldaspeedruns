from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def social_identity(context, provider, user=None):
    if not user:
        user = context.request.user

    if provider in user.profile.social_identities:
        provider_identity = user.profile.social_identities[provider]
        if provider_identity['visible']:
            return provider_identity.get('identity')

    return None
