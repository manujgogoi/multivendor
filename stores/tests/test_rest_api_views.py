from django.http import request
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient
from rest_framework_simplejwt.tokens import RefreshToken
from stores.models import Product
from stores.views import ProductViewSet
from vendor.models import Vendor

User = get_user_model()

class ProductTestCase(APITestCase):

    def setUp(self):
        
        # Create an user
        self.aUser = User.objects.create(email="test@user.com", password='123')
        self.aVendor = Vendor.objects.create(name="A Vendor", owner=self.aUser)
        self.tokens = self.get_tokens_for_user(self.aUser)
        self.api_authentication()

    # Authentication
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])
        
    # get Simple JWT Tokens
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_create_product_authenticated(self):
        product = {'title': 'A Product', 'regular_price': '900'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_unauthenticated(self):
        self.client.force_authenticate(user=None)
        product = {'title': 'A Product', 'regular_price': '900'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_without_vendor(self):
        
        # Create another user
        bUser = User.objects.create(email="b@user.com", password="123")
        
        # bUser has no vendor
        # authenticate bUser to create products
        self.tokens = self.get_tokens_for_user(bUser)
        self.api_authentication()

        # Now try to create a product
        product = {'title': 'B Product', 'regular_price': '2000'}
        
        with self.assertRaises(AttributeError):
            response = self.client.post("/api/store/products/", product)
        
    
    def test_products_list(self):
        
        # Create three products
        product = {'title': 'A Product', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = {'title': 'B Product', 'regular_price': '950'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get all products Test
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # qs = Product.objects.all()
        # self.assertEqual(qs.count(), 3)

        # Get Single product Test
        response = self.client.get(reverse('product-detail', kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "A Product")

        # Get vendor Test (NOT MANDATORY)
        # vendor_link = response.data['vendor']
        # request = RequestsClient()
        # response = self.client.get(vendor_link)
        # self.assertEqual(response.data['name'], self.aVendor.name)


    def test_product_detail(self):
        
        # Create a product
        product = {'title': 'A Product', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get product detail
        response = self.client.get(reverse("product-detail", kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], product['title'])


    def test_product_update_by_owner(self):
        # Create a product
        product = {'title': 'A Product', 'description': 'No description', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update product
        updated_product = {'title': 'An updated product', 'regular_price': '2000'}
        response = self.client.put(reverse('product-detail', kwargs={'pk':1}), updated_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check product
        response = self.client.get(reverse('product-detail', kwargs={'pk':1}))
        self.assertEqual(response.data['title'], updated_product['title'])
        self.assertEqual(response.data['description'], product['description'])

        # Partial update
        updated_product = {'title': 'A partially updated product'}
        response = self.client.patch(reverse('product-detail', kwargs={'pk':1}), updated_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check product
        response = self.client.get(reverse('product-detail', kwargs={'pk':1}))
        self.assertEqual(response.data['title'], updated_product['title'])
        self.assertEqual(response.data['description'], product['description'])


    def test_product_update_by_random_user(self):
         # Create a product
        product = {'title': 'A Product', 'description': 'No description', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Login as a random user
        random_user = User.objects.create_user(email="random@user.com", password="123")
        self.client.force_authenticate(user=random_user)

        # Update product
        updated_product = {'title': 'An updated product', 'regular_price': '2000'}
        response = self.client.put(reverse('product-detail', kwargs={'pk':1}), updated_product)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_product_delete_by_owner(self):
        # Create a product
        product = {'title': 'A Product', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Delete the product
        response = self.client.delete(reverse("product-detail", kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
    def test_product_delete_by_random_user(self):

        # Create a product
        product = {'title': 'A Product', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Login as a random user
        random_user = User.objects.create_user(email="random@user.com", password="123")
        self.client.force_authenticate(user=random_user)

        # Delete the product
        response = self.client.delete(reverse("product-detail", kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryTestCase(APITestCase):
    
    def setUp(self):
        # Create a staffuser
        self.staffUser = User.objects.create_staffuser(email="staff@user.com", password="123")

        # Authenticate
        self.tokens = self.get_tokens_for_user(self.staffUser)
        self.api_authentication()

        # Create some Categories
        category1 = {'title': 'Category-1'}
        self.client.post(reverse('category-list'), category1)

        category2 = {'title': 'Category-2'}
        self.client.post(reverse('category-list'), category2)

        category3 = {'title': 'Category-3'}
        self.client.post(reverse('category-list'), category3)

        # Create an user
        self.aUser = User.objects.create(email="test@user.com", password='123')
        self.aVendor = Vendor.objects.create(name="A Vendor", owner=self.aUser)
        self.tokens = self.get_tokens_for_user(self.aUser)
        self.api_authentication()

    # Authentication
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])
        
    # get Simple JWT Tokens
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


    def test_list_category_by_anyone(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_add_category_by_an_user(self):
        category = {'title': 'A category'}
        response = self.client.post(reverse('category-list'), category)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_by_an_user(self):
        updated_category = {'title': 'An updated category'}
        response = self.client.put(reverse('category-detail', kwargs={'pk':1}), updated_category)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_by_an_user(self):
        response = self.client.delete(reverse('category-detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
class SpecificationTestCase(APITestCase):
    
    def setUp(self):
        # Create a staffuser
        self.staffUser = User.objects.create_staffuser(email="staff@user.com", password="123")

        # Authenticate
        self.tokens = self.get_tokens_for_user(self.staffUser)
        self.api_authentication()

        # Create a Category
        category1 = {'title': 'Category-1'}
        self.client.post(reverse('category-list'), category1)

        # Create an user and a vendor
        self.aUser = User.objects.create(email="test@user.com", password='123')
        self.aVendor = Vendor.objects.create(name="A Vendor", owner=self.aUser)
        
        # Authenticat the user
        self.tokens = self.get_tokens_for_user(self.aUser)
        self.api_authentication()

    # Authentication
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])
        
    # get Simple JWT Tokens
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_create_specification_for_a_product(self):
        
        # Create a product
        product = {'title': 'A Product', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the product
        response = self.client.get(reverse('product-detail', kwargs={'pk':1}))
        
        product_url = response.data['url']

        # As we are using HyperlinkedModelSerializer in backend
        # we use 'url' instead of 'id' for relationships

        # Create a specification for the above product
        spec = {'name': 'color', 'value': 'red', 'product': product_url }
        response = self.client.post(reverse('specification-list'), spec)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a specification without any product
        response = self.client.post(reverse('specification-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_specification_by_random_user(self):
        # Create a product
        product = {'title': 'A Product', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the product
        response = self.client.get(reverse('product-detail', kwargs={'pk':1}))
        
        product_url = response.data['url']
        
        # Create and authenticate a random user
        random_user = User.objects.create_user(email="random@user.com", password="123")
        self.client.force_authenticate(user=random_user)
        

        # Try to create the specification of a product that is 
        # owned by a different vendor/user
        spec = {'name': 'color', 'value': 'red', 'product': product_url }
        response = self.client.post(reverse('specification-list'), spec)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_specification_by_product_owner(self):
        # Create a product
        product = {'title': 'A Product', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the product
        response = self.client.get(reverse('product-detail', kwargs={'pk':1}))
        product_url = response.data['url']

        # Create a specification for the above product
        spec = {'name': 'color', 'value': 'red', 'product': product_url }
        response = self.client.post(reverse('specification-list'), spec)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update the specification
        updated_spec = {'name': 'colour', 'value': 'Yellow', 'product': product_url}
        response = self.client.put(reverse('specification-detail', kwargs={'pk':1}), updated_spec)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Partial Update (Error)
        updated_spec = {'value': 'Yellow'}
        response = self.client.put(reverse('specification-detail', kwargs={'pk':1}), updated_spec)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Partial Update using patch (OK)
        response = self.client.patch(reverse('specification-detail', kwargs={'pk':1}), updated_spec)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_specification_by_product_owner(self):
        # Create a product
        product = {'title': 'A Product', 'regular_price': '1000'}
        response = self.client.post("/api/store/products/", product)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the product
        response = self.client.get(reverse('product-detail', kwargs={'pk':1}))
        product_url = response.data['url']

        # Create a specification for the above product
        spec = {'name': 'color', 'value': 'red', 'product': product_url }
        response = self.client.post(reverse('specification-list'), spec)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Get the specification
        response = self.client.get(reverse('specification-detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete the specification
        response = self.client.delete(reverse('specification-detail', kwargs={'pk':response.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get the specification again
        response = self.client.get(reverse('specification-detail', kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)