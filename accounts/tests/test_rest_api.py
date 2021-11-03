import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.views import UserViewSet
from accounts.models import User as UserModel

User = get_user_model()

class RegistrationTestCase(APITestCase):
    
    def test_registration(self):
        data = {'email': 'test@user.com', 'password': '123'}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_without_email_password(self):
        data = {}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_email(self):
        data = {'email': 'testemail.com', 'password': '123'}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_only_with_email(self):
        data = {'email': 'test@user.com', 'password': ''}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_only_with_password(self):
        data = {'email': '', 'password': '123'}
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_existing_email(self):
        user1 = {'email': 'test@user.com', 'password': '123'}
        user2 = {'email': 'test@user.com', 'password': '111'}
        response1 = self.client.post("/api/users/", user1)
        response2 = self.client.post("/api/users/", user2)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoggedInTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='test@user.com', password='123')

    def test_change_email(self):

        # User Login
        data = {'email': 'test@user.com', 'password': '123'}
        response = self.client.post("/api/token/", data)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

        # Change Email id
        data = {'email': 'new@email.com'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(f"/api/users/{self.user.id}/change_email/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        userUpdated = User.objects.get(pk=self.user.id)
        self.assertNotEqual(self.user.email, userUpdated.email)

    def test_change_with_invalid_email_(self):

        # User Login
        data = {'email': 'test@user.com', 'password': '123'}
        response = self.client.post("/api/token/", data)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

        # Change Email id
        data = {'email': 'invalid_email'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(f"/api/users/{self.user.id}/change_email/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_change_with_existing_email_(self):

        # Create a new user
        anotherUser = User.objects.create_user(email='existing@user.com', password='123')

        # User Login
        data = {'email': 'test@user.com', 'password': '123'}
        response = self.client.post("/api/token/", data)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

        # Change Email id
        data = {'email': anotherUser.email}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(f"/api/users/{self.user.id}/change_email/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_change_password(self):

        # User Login
        data = {'email': 'test@user.com', 'password': '123'}
        response = self.client.post("/api/token/", data)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

        # Change password
        data = {'old_password': '123', 'new_password': '321'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(f"/api/users/{self.user.id}/change_password/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_with_existing_password(self):

        # User Login
        data = {'email': 'test@user.com', 'password': '123'}
        response = self.client.post("/api/token/", data)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

        # Change password
        data = {'old_password': '123', 'new_password': '123'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(f"/api/users/{self.user.id}/change_password/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_with_wrong_old_password(self):

        # User Login
        data = {'email': 'test@user.com', 'password': '123'}
        response = self.client.post("/api/token/", data)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

        # Change password
        data = {'old_password': 'wrong_password', 'new_password': '321'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(f"/api/users/{self.user.id}/change_password/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    