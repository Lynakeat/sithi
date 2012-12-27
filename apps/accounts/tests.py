import time
from django.test import TestCase
from apps.accounts.forms import RegistrationForm, LoginForm
from apps.accounts.models import SubscribeLocation, Account

class RegistrationFormTest(TestCase):
    def test_registration_form_validation(self):
        """ Test creation of an Account, and make sure duplicate (and 
        case-insensitive matching) accounts cannot be created 
        """
        VALID_EMAIL_ADDRESS = 'foo@example.com'
        # case-insensitive match to VALID_EMAIL_ADDRESS
        CORRESPONDING_EMAIL_ADDRESS = 'Foo@example.com'
        # longer than 30 characters, the limit for the `username` field on the model
        LONG_EMAIL_ADDRESS = 'someverylongemailaddress@example.com'
        # unique address matching first 30 characters of LONG_EMAIL_ADDRESS
        LONG_EMAIL_ADDRESS_MATCHING_FIRST_30_CHARS = 'someverylongemailaddress@example.net'

        # create a sample Location, necessary to save an Account
        my_location = SubscribeLocation(name='Foo Location',cmonitor_name='FooLocation')
        my_location.save()

        account_dict = {
            'name': 'Foo Bar', 
            'email': VALID_EMAIL_ADDRESS, 
            'password1': 'foobar',
            'password2': 'foobar',
            'is_agree': True,
            'subscribe_location': [my_location.pk],
            # pass the timestamp check (not older than 2 hours, not newer than 9 seconds)
            'timestamp': int(time.time())-10, 
            'referred_email': 'someone@example.com'
            # omit honeypot to pass
        }
        first_reg = RegistrationForm(data=account_dict)
        self.assertEqual(first_reg.errors, {}) # this will display any errors
        self.assertEqual(first_reg.is_valid(), True)
        # save the valid account
        account1 = first_reg.save()

        # make sure some attributes of the account are correct
        self.assertEqual(account1.email, account_dict['email'])
        self.assertEqual(account1.username, account_dict['email'])

        # create a new account, with the same email address
        duplicate_reg = RegistrationForm(data=account_dict)
        # assert a form error, indicating that email address is already used
        self.assertEqual(duplicate_reg.errors['email'][0], u'A user with that email already exists.')
        self.assertEqual(duplicate_reg.is_valid(), False)

        # create a new account, with a matching (case-insensitive) email address
        corresponding_reg = RegistrationForm(data=dict(account_dict, email=CORRESPONDING_EMAIL_ADDRESS))
        # assert a form error, indicating that email address is already used
        self.assertEqual(corresponding_reg.errors['email'][0], u'A user with that email already exists.')
        self.assertEqual(corresponding_reg.is_valid(), False)

        # create an account with an email address
        long_email_reg = RegistrationForm(data=dict(account_dict, email=LONG_EMAIL_ADDRESS))
        self.assertEqual(long_email_reg.errors, {}) # this will display any errors
        self.assertEqual(long_email_reg.is_valid(), True)
        account_long = long_email_reg.save()
        # make sure the first 30 characters of the email address are saved as the username
        self.assertEqual(account_long.username, account_long.email[:30])

        # attempt to create an account for an email address, the first 30 
        # characters of which match the first 30 characters of account_long's
        # username.  the account should save, but with a unique username.
        long_email_reg2 = RegistrationForm(data=dict(account_dict, email=LONG_EMAIL_ADDRESS_MATCHING_FIRST_30_CHARS))
        self.assertEqual(long_email_reg2.errors, {}) # this will display any errors
        self.assertEqual(long_email_reg2.is_valid(), True)
        account_long2 = long_email_reg2.save()

        # make sure the usernames don't match
        self.assertEqual(False, account_long.username == account_long2.username)


class LoginFormTest(TestCase):

    def test_login_form_validation(self):
        """ Allow username of another capitalization to authenticate """

        VALID_EMAIL_ADDRESS = 'foo@example.com'
        CORRESPONDING_EMAIL_ADDRESS = 'Foo@example.com' # case-insensitive match
        OTHER_EMAIL_ADDRESS = 'notfoo@example.com'
        PASSWORD = 'foobar'

        # create a sample Location, necessary to save an Account
        my_location = SubscribeLocation(name='Foo Location',cmonitor_name='FooLocation')
        my_location.save()

        account_dict = {
            'first_name': 'Foo', 
            'last_name': 'Bar',
            'email': VALID_EMAIL_ADDRESS, 
            'username': VALID_EMAIL_ADDRESS,
        }

        account = Account.objects.create(**account_dict)
        account.save()
        account.set_password(PASSWORD)
        account.save()

        # verify that user can log in with those credentials
        auth_attempt = LoginForm(data={'email':VALID_EMAIL_ADDRESS, 'password':PASSWORD})
        self.assertEqual(auth_attempt.errors, {}) # this will display any errors
        self.assertEqual(auth_attempt.is_valid(), True)
        # attempt with case-insensitive match for email address
        auth_attempt = LoginForm(data={'email':CORRESPONDING_EMAIL_ADDRESS, 'password':PASSWORD})
        self.assertEqual(auth_attempt.errors, {}) # this will display any errors
        self.assertEqual(auth_attempt.is_valid(), True)
        # attempt to login with wrong email address
        auth_attempt = LoginForm(data={'email':OTHER_EMAIL_ADDRESS, 'password':PASSWORD})
        self.assertEqual(auth_attempt.is_valid(), False)
