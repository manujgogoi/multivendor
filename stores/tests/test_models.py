from django.contrib.auth import get_user_model
from django.test import TestCase
from vendor.models import Vendor
from stores.models import Category, Product

User = get_user_model()


def create_user(email, password):
    return User.objects.create_user(email=email, password=password)

def create_vendor(name, is_active, owner):
    return Vendor.objects.create(name=name, is_active=is_active, owner=owner)

def create_category(title, is_active, parent=None):
    return Category.objects.create(title=title, is_active=is_active, parent=parent)

class CategoryTestCase(TestCase):

    def setUp(self):

        # Create an User
        self.user = create_user(email='test@user.com', password='123')

        # Create a vendor
        self.active_vendor = create_vendor(name='A vendor', is_active=True, owner=self.user)

        # Create a Category
        self.category = create_category(title="A Category", is_active=True)


    def test_create_category(self):
        category = Category.objects.get(pk=self.category.id)
        self.assertEqual(category.title, 'A Category')
        self.assertEqual(category.parent, None)

    def test_create_child_category(self):
        child_cat = create_category(title="Child category", is_active=True, parent=self.category)
        child_cat = Category.objects.get(pk=child_cat.id)
        self.assertEqual(child_cat.title, 'Child category')
        self.assertEqual(child_cat.parent, self.category)


class ProductTestCase(TestCase):

    def setUp(self):
        
        # Create an User
        self.user = create_user(email='test@user.com', password='123')

        # Create a vendor
        self.vendor = create_vendor(name='A vendor', is_active=True, owner=self.user)

        # Create a Category
        self.category = create_category(title="A Category", is_active=True)

        # Create a Product
        self.product = Product.objects.create(
                                                title="A product",
                                                regular_price=5000,
                                                category=self.category,
                                                vendor=self.vendor)

    def test_create_product(self):
        product = Product.objects.get(pk=self.product.id)
        self.assertEqual(product.title, 'A product')
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.vendor, self.vendor)

    def test_update_product(self):
        self.product.title = 'Updated product title'
        self.product.save()
        product = Product.objects.get(pk=self.product.id)
        self.assertEqual(product.title, 'Updated product title')

        # Update product category
        # Create a new category
        category = create_category(title="New category", is_active=True)
        
        # Chnage product category
        self.product.category = category
        self.product.save()

        # Test
        product = Product.objects.get(pk=self.product.id)
        self.assertEqual(product.category, category)


    def test_product_for_deleted_category(self):
        
        # Delete the category
        self.category.delete()

        product = Product.objects.get(pk=self.product.id)
        category = product.category if hasattr(product, 'category') else None
        self.assertNotEqual(category, self.category)