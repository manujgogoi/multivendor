from django.test import TestCase
from vendor.models import Vendor
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

# Create your tests here.

class VendorTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@user.com", password="123")
        self.vendor = Vendor.objects.create(name="testVendor", owner=self.user)

    def test_create_vendor(self):
        vendor = Vendor.objects.get(name__exact='testVendor')
        self.assertEqual(vendor.name, 'testVendor')
        self.assertFalse(vendor.is_active)
        self.assertFalse(vendor.is_verified)
        self.assertEqual(str(vendor), 'testVendor')
 

    def test_create_multiple_vendor_for_a_single_user(self):
        # Creating multiple vendor for a single user causes error. 
        # One user can create one vendor only
        with self.assertRaises(IntegrityError):
            Vendor.objects.create(name="anotherVendor", owner=self.user)
        

    def test_create_vendor_without_an_owner(self):
        
        # Column 'owner_id' cannot be null
        with self.assertRaises(IntegrityError):
            Vendor.objects.create(name="anotherVendor")


    def test_update_vendor(self):
        self.vendor.name="new vendor name"
        self.vendor.save()
        self.assertEqual(self.vendor.name, 'new vendor name')


    def test_delete_vendor(self):
        self.vendor.delete()

