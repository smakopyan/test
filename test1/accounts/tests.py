from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Role, BusinessElement, AccessRule
import json

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user_role = Role.objects.create(name='user')
        
        self.products_element = BusinessElement.objects.create(name='products')
        
        AccessRule.objects.create(
            role=self.user_role,
            element=self.products_element,
            read_permission=True,
            # read_all_permission=True,
            create_permission=False,
            update_permission=False,
            # update_all_permission=False,
            delete_permission=False,
            # delete_all_permission=False
        )
        
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role=self.user_role
        )

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_access_protected_resource(self):
        login_url = reverse('login')
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['token']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        products_url = reverse('products')
        response = self.client.get(products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_without_token(self):
        products_url = reverse('products')
        response = self.client.get(products_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        products_url = reverse('products')
        response = self.client.get(products_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizationTests(APITestCase):
    def setUp(self):
        self.user_role = Role.objects.create(name='user')
        self.admin_role = Role.objects.create(name='admin')
        
        self.products_element = BusinessElement.objects.create(name='products')
        self.users_element = BusinessElement.objects.create(name='users')
        
        AccessRule.objects.create(
            role=self.user_role,
            element=self.products_element,
            read_permission=True,
            # read_all_permission=True,
            create_permission=False,
            update_permission=False,
            # update_all_permission=False,
            delete_permission=False,
            # delete_all_permission=False
        )
        
        AccessRule.objects.create(
            role=self.admin_role,
            element=self.users_element,
            read_permission=True,
            # read_all_permission=True,
            create_permission=True,
            update_permission=True,
            # update_all_permission=True,
            delete_permission=True,
            # delete_all_permission=True
        )
        
        # Создаем тестовых пользователей
        self.user = CustomUser.objects.create_user(
            email='user@example.com',
            password='userpass123',
            first_name='Regular',
            last_name='User',
            role=self.user_role
        )
        
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
            role=self.admin_role
        )

    def test_user_access_to_permitted_resource(self):
        login_url = reverse('login')
        login_data = {'email': 'user@example.com', 'password': 'userpass123'}
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['token']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        products_url = reverse('products')
        response = self.client.get(products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_access_to_restricted_resource(self):
        login_url = reverse('login')
        login_data = {'email': 'user@example.com', 'password': 'userpass123'}
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['token']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        users_url = reverse('users')
        response = self.client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_access_to_restricted_resource(self):
        login_url = reverse('login')
        login_data = {'email': 'admin@example.com', 'password': 'adminpass123'}
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['token']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        users_url = reverse('users')
        response = self.client.get(users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)