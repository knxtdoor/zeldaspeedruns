from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from accounts.utils import hashid_encode


class User(AbstractUser):
    @property
    def hashid(self):
        return hashid_encode(self.__class__, self.id)

    def __str__(self):
        return self.username


class ProfileManager(models.Manager):
    def create_profile(self, user):
        if not user:
            raise ValueError('The user must be set')

        profile = self.model(user=user, social_identities={})
        profile.full_clean()
        profile.save(using=self._db)

        return profile


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    avatar = models.ImageField(
        upload_to='avatars',
        null=True,
        blank=True,
        help_text=_('Profile picture that displays besides your name.'),
    )
    social_identities = models.JSONField(default=dict, blank=True)

    objects = ProfileManager()

    def remove_social_identity(self, provider):
        if provider is None:
            return

        if provider in self.social_identities:
            del self.social_identities[provider]

    def update_social_identity(self, provider, identity, **kwargs):
        if provider is None:
            raise ValueError('provider must be set')
        if identity is None:
            raise ValueError('identity must be set')

        visible = True
        if provider in self.social_identities:
            visible = self.social_identities[provider]

        self.social_identities[provider] = {
            'provider': provider,
            'identity': identity,
            'visible': visible,
            **kwargs,
        }

    def clean(self):
        super(Profile, self).clean()
        for provider in self.social_identities:
            identity = self.social_identities[provider]
            if 'visible' not in identity or type(identity['visible']) != bool:
                raise ValidationError('identity {} must have key visible set and be of type bool'.format(identity))
            if 'provider' not in identity or type(identity['provider']) != str:
                raise ValidationError('identity {} must have key provider set and be of type str'.format(identity))
            if 'identity' not in identity:
                raise ValidationError('identity {} must have key identity set'.format(identity))

    def __str__(self):
        return self.user.username


# TODO: This should probably live in its own file
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create_profile(user=instance)


class ConfirmationTokenManager(models.Manager):
    def create_token(self, email, user=None):
        if not email:
            raise ValueError('The email address must be set.')

        email = get_user_model().objects.normalize_email(email)

        token = self.model(
            email=email,
            user=user,
            code=get_random_string(32),
            expires_at=timezone.now() + timezone.timedelta(hours=1),
        )
        token.full_clean()
        token.save(using=self._db)

        return token

    def get_token_for_email(self, email):
        if not email:
            raise ValueError('The email address must be set')

        token = self.filter(email=email).order_by('-created_at').first()

        return token


class ConfirmationToken(models.Model):
    """
    Confirmation tokens are used to confirm the validity of an user's communication method.
    """
    email = models.EmailField(
        validators=[validate_email]
    )
    code = models.CharField(
        unique=True,
        max_length=32,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    objects = ConfirmationTokenManager()

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.user is not None and self.user.email == self.email:
            raise ValidationError('Email cannot be the same as user email.')

    def is_valid_for_user(self, user):
        return self.is_valid and self.is_email_change and self.user == user

    @property
    def is_email_change(self):
        return self.user is not None

    @property
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        return '{} ({})'.format(self.code, self.email)
