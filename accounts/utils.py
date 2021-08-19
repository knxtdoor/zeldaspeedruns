from django.conf import settings
from django.utils.crypto import get_random_string
from hashids import Hashids


def hashid_encode(cls, *values):
    """Encodes a value as a hashid unique for the class."""
    return Hashids(
        salt=settings.SECRET_KEY + str(cls),
        min_length=16,
    ).encode(*values)
