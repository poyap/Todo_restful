from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

class SignUpAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:signup')
        self.valid_payload = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpass', 'role': 1}
        self.invalid_payload = {'username': '', 'email': '', 'password': '', 'role': ''}
        
    def test_create_user_with_valid_data(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_user_with_invalid_data(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
