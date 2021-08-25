from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Profile


class ProfileTests(TestCase):
    def test_creation_fails_with_no_user(self):
        self.assertRaises(ValueError, Profile.objects.create_profile, user=None)

    def test_profile_is_created_on_user_save(self):
        user = get_user_model().objects.create_user(username='profiletest', email='profile@example.com')
        user.refresh_from_db()
        self.assertIsNot(user.profile, None)

    def test_profile_social_identity_is_created(self):
        user = get_user_model().objects.create_user(username='profiletest', email='profile@example.com')
        user.profile.update_social_identity('test', 'testidentity')
        self.assertIs(user.profile.social_identities['test']['identity'], 'testidentity')

    def test_profile_social_identity_is_removed(self):
        user = get_user_model().objects.create_user(username='profiletest', email='profile@example.com')
        user.profile.update_social_identity('test', 'testidentity')
        user.profile.remove_social_identity('test')
        self.assertIsNone(user.profile.social_identities.get('test'))

    def test_social_identity_must_fail_validation_if_invalid(self):
        user = get_user_model().objects.create_user(username='profiletest', email='profile@example.com')
        user.profile.update_social_identity(True, True)
        self.assertRaises(ValidationError, user.profile.full_clean)

    def test_update_social_identity_must_fail_with_none_arg(self):
        user = get_user_model().objects.create_user(username='profiletest', email='profile@example.com')
        self.assertRaises(ValueError, user.profile.update_social_identity, provider=None, identity=None)

    def test_update_social_identity_sets_kwargs(self):
        user = get_user_model().objects.create_user(username='profiletest', email='profile@example.com')
        user.profile.update_social_identity('test', 'testidentity', extra_value=10)
        self.assertIs(user.profile.social_identities['test']['extra_value'], 10)
