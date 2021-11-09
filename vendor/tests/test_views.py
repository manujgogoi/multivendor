from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from vendor.models import Vendor
from django.contrib.auth import get_user_model

User = get_user_model()

class VendorViewSetTestCase(APITestCase):

    def setUp(self):

        # Create s user
        self.user1 = User.objects.create_user(email="user1@test.com", password="123")
    
        # User Login
        url="/api/token/"     
        data = {'email': 'user1@test.com', 'password': '123'}
        self.token = self.client.post(url, data)
        self.assertTrue("access" in self.token.data)
        self.assertTrue("refresh" in self.token.data)

        # Create a Vendor
        url=reverse('vendor-list')
        vendor_data = {'name': 'A vendor'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.data['access'])
        response = self.client.post(url, vendor_data)
        self.vendor_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def tearDown(self):
    #     self.client.credentials()

    def test_get_vendor_detail_by_self(self):
        url=reverse('vendor-detail', kwargs={'pk': self.vendor_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vendor_detail_by_other_user(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor_id})
        
        # Log out current user (make user anonymous)
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Activate vendor
        vendor = Vendor.objects.get(pk=self.vendor_id)
        vendor.is_active = True
        vendor.save()

        # Get vendor detail
        response = self.client.get(url)
        self.assertEqual('A vendor', response.data['name'])


    def test_create_more_vendor_by_same_user(self):
        
        # Try to create another Vendor
        # It should not permit to create
        url=reverse('vendor-list')
        vendor_data = {'name': 'Another vendor'}
        response = self.client.post(url, vendor_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_change_vendor_name(self):

        url=reverse('vendor-detail', kwargs={'pk' : self.vendor_id})
        new_vendor_name = {'name' : 'New vendor name'}
        response = self.client.put(url, new_vendor_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_vendor_name['name'], response.data['name'])


    def test_change_vendor_name_by_un_authorized_user(self):
        # create a different user
        User.objects.create_user(email="user2@test.com", password="123")

        # Login that user
        url="/api/token/"     
        data = {'email': 'user2@test.com', 'password': '123'}
        token = self.client.post(url, data)
        self.assertTrue("access" in self.token.data)
        self.assertTrue("refresh" in self.token.data)

        # Try to change vendor name of another user
        url=reverse('vendor-detail', kwargs={'pk' : self.vendor_id})
        
        new_vendor_name = {'name' : 'Updated vendor name'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])
        response = self.client.put(url, new_vendor_name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_vendor_list(self):
        # Create two users
        user2 = User.objects.create_user(email="user2@test.com", password="123")
        user3 = User.objects.create_user(email="user3@test.com", password="123")


        # Create two active vendors
        # setUp() will automatically create an inactive vendor called `A vendor`
        # When users request vendor list, they should get only active vendors
        # So this test ensures that only active vendors will be in the list

        Vendor.objects.create(name="User 2 vendor", is_active=True, owner=user2)
        Vendor.objects.create(name="User 3 vendor", is_active=True, owner=user3)

        url = reverse('vendor-list')

        self.client.credentials()
        response = self.client.get(url)

        total = len(response.data)

        self.assertEqual(total, 2)


    def test_delete_vendor_by_itself(self):
        url = reverse('vendor-detail', kwargs={'pk' : self.vendor_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_vendor_by_other_user(self):
        
        # Activate vendor to make it accessible for other users
        vendor = Vendor.objects.get(pk=self.vendor_id)
        vendor.is_active = True
        vendor.save()
        
        url = reverse('vendor-detail', kwargs={'pk' : self.vendor_id})
        
        # Make user anonymous
        self.client.credentials()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Create a new user
        user2 = User.objects.create_user(email="xyz@abc.com", password="123")
        
        # Login user2
        url="/api/token/"     
        data = {'email': 'xyz@abc.com', 'password': '123'}
        token = self.client.post(url, data)
        # self.assertTrue("access" in self.token.data)
        # self.assertTrue("refresh" in self.token.data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])

        # Now try to delete vendor
        url = reverse('vendor-detail', kwargs={'pk' : self.vendor_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)