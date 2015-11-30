from django.contrib.auth.models import User
from django.test import TestCase

from oauth2_provider.models import Application

import json

TESTING_APP_CLIENT_ID = 'sample_id'
TESTING_APP_CLIENT_SECRET = 'sample_secret'


class RegistrationTest(TestCase):
    def setUp(self):
        # Create a mock user of the app
        user = User.objects.create_user(
            username='test_username',
            email='test_email@email.com',
            password='passwordhehehe'
        )

        # Create a mock of the application
        Application.objects.create(
            user=user,
            name='Namnam Android',
            client_id=TESTING_APP_CLIENT_ID,
            client_secret=TESTING_APP_CLIENT_SECRET,
            client_type='confidential',
            authorization_grant_type='password',
            redirect_uris='',
        )

    def test_works_with_valid_data(self):
        url = '/api-auth/signup/'
        data = {
            "username": "a_valid_username",
            "email": "a_valid_email@testing.com",
            "password": "alegitpassword",
            "client_id": TESTING_APP_CLIENT_ID,
            "client_secret": TESTING_APP_CLIENT_SECRET
        }

        response = self.client.post(
            url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        try:
            json.loads(response.content)
            self.assertTrue('access_token' in response.content)
        except ValueError:
            self.fail('Response body is not a valid JSON')

        try:
            User.objects.get(
                username=data['username'], email=data['email'])
        except User.DoesNotExist:
            self.fail('Created user doesn\'t exist in the database')

    def test_works_with_facebook_data(self):
        url = '/api-auth/signin-fb/'
        data = {
            "id": 13809124278394,
            "name": "Facebook Name",
            "email": "facebook_email@facebook.com",
            "client_id": TESTING_APP_CLIENT_ID,
            "client_secret": TESTING_APP_CLIENT_SECRET
        }

        response = self.client.post(
            url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        try:
            json.loads(response.content)
            self.assertTrue('access_token' in response.content)
        except ValueError:
            self.fail('Response body is not a valid JSON')

        try:
            User.objects.get(
                username=data['email'].split('@')[0], email=data['email'])
        except User.DoesNotExist:
            self.fail('Created user doesn\'t exist in the database')

    def test_works_with_google_data(self):
        url = '/api-auth/signin-google/'
        data = {
            "id": 53809342308394,
            "name": "Google Name",
            "email": "google_email@google.com",
            "client_id": TESTING_APP_CLIENT_ID,
            "client_secret": TESTING_APP_CLIENT_SECRET
        }

        response = self.client.post(
            url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        try:
            json.loads(response.content)
            self.assertTrue('access_token' in response.content)
        except ValueError:
            self.fail('Response body is not a valid JSON')

        try:
            User.objects.get(
                username=data['email'].split('@')[0], email=data['email'])
        except User.DoesNotExist:
            self.fail('Created user doesn\'t exist in the database')
