from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from accounts.utils import hashid_encode


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars',
        null=True,
        help_text=_('Profile picture that displays besides your name.'),
    )

    @property
    def hashid(self):
        return hashid_encode(self.__class__, self.id)

    def __str__(self):
        return self.username
