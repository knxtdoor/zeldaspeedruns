from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from accounts.models import ConfirmationToken, Profile


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


class ConfirmationTokenTests(TestCase):
    test_username = 'testuser'
    test_email = 'test@example.com'

    def test_creation_must_fail_with_no_arguments(self):
        self.assertRaises(ValueError, ConfirmationToken.objects.create_token, email=None)

    def test_creation_must_fail_with_invalid_email(self):
        email = 'invalidemail.com 134'
        self.assertRaises(ValidationError, ConfirmationToken.objects.create_token, email=email)

    def test_creation_must_fail_with_identical_user_email(self):
        user = get_user_model().objects.create_user(
            username=self.test_username,
            email=self.test_email,
        )

        self.assertRaises(
            ValidationError,
            ConfirmationToken.objects.create_token,
            email=self.test_email,
            user=user,
        )

    def test_new_token_must_expire_in_the_future(self):
        token = ConfirmationToken.objects.create_token(self.test_email)
        self.assertIs(token.expires_at >= timezone.now(), True)

    def test_get_token_for_email_must_return_most_recent_token(self):
        token1 = ConfirmationToken.objects.create_token(self.test_email)
        token2 = ConfirmationToken.objects.create_token(self.test_email)

        token = ConfirmationToken.objects.get_token_for_email(self.test_email)
        self.assertIs(token.code != token1.code and token.code == token2.code, True)

    def test_code_is_only_usable_by_user(self):
        user1 = get_user_model().objects.create_user(username='test_user1', email='user1@example.com')
        user2 = get_user_model().objects.create_user(username='test_user2', email='user2@example.com')
        token = ConfirmationToken.objects.create_token(email='test@example.com', user=user1)
        self.assertIs(token.is_valid_for_user(user2), False)


class EmailChangeViewTests(TestCase):
    def test_reject_invalid_code(self):
        code = get_random_string(32)
        url = reverse('accounts:email_change', args=(code,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
