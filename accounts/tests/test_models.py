from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

User = get_user_model()

class UserTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@user.com', password='123')
        self.assertEqual(user.email, 'test@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Test for no username field exists
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(ValueError):
            User.objects.create_user(email='')

        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='123')

        with self.assertRaises(ValueError):
            User.objects.create_user(email='test@user.com', password='')


    def test_create_staffuser(self):
        user = User.objects.create_staffuser(email='test@user.com', password='123')
        self.assertEqual(user.email, 'test@user.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Test for no username field exists
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_staffuser()

        with self.assertRaises(ValueError):
            User.objects.create_staffuser(email='')

        with self.assertRaises(ValueError):
            User.objects.create_staffuser(email='', password='123')

        with self.assertRaises(ValueError):
            User.objects.create_staffuser(email='test@user.com', password='')

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='test@user.com', password='123')
        self.assertEqual(user.email, 'test@user.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        # Test for no username field exists
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_superuser()

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='')

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='', password='123')

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='test@user.com', password='')

    def test_user_str_is_email(self):
        user = User.objects.create(email='test@user.com', password='123')
        self.assertEqual(str(user), user.email)

    def test_user_get_full_name(self):
        user = User.objects.create(email='test@user.com', password='123')
        self.assertEqual(user.get_full_name(), user.email)

    def test_user_get_short_name(self):
        user = User.objects.create(email='test@user.com', password='123')
        self.assertEqual(user.get_short_name(), user.email)  


    def test_user_has_perm(self):
        user = User.objects.create(email='test@user.com', password='123')
        
        # More testing required if user permissions is modified
        self.assertTrue(user.has_perm('accounts.add_User'))  

    def test_user_has_module_perm(self):
        user = User.objects.create(email='test@user.com', password='123')
        self.assertTrue(user.has_module_perms('accounts'))  



# class UserTestCase(TestCase):

#     def setUp(self):
#         self.user_pass = '1234'
#         self.email = 'mg@email.com'
#         self.user_a = User.objects.create_user(email = self.email, password=self.user_pass)

#     def test_user_is_created(self):
#         '''
#         Check if setUp() created a user or not.
#         '''
#         user_count = User.objects.all().count()
#         self.assertEqual(user_count, 1)
#         self.assertNotEqual(user_count, 0)
#         self.assertFalse(self.user_a.is_staff)
#         self.assertFalse(self.user_a.is_superuser)

#     def test_user_email_and_password(self):
#         '''
#         Check password match of an existing user
#         using check_password() method
#         '''
#         user_a = User.objects.get(email=self.email)
#         self.assertTrue(user_a.check_password(self.user_pass))


#     def test_user_duplicate_email(self):
#         '''
#         This test is intended to raise an AssertionError if no IntegrityError is
#         raised (i.e. no IntegrityError == an AssertionError == no duplicate field).
#         We are creating a new user by existing email id.
#         '''

#         with self.assertRaises(IntegrityError):
#             user_new = User.objects.create_user(email=self.email, password=self.user_pass)

    
#     def test_user_create_a_staffuser(self):
#         '''
#         Create and test a staff user
#         '''
#         user_staff = User.objects.create_staffuser(email='m2@email.com', password=self.user_pass)
#         self.assertTrue(user_staff.is_staff)
#         self.assertFalse(user_staff.is_superuser)

#     def test_user_create_a_superuser(self):
#         '''
#         Create and test a superuser
#         '''
#         user_superuser = User.objects.create_superuser(email='m3@email.com', password=self.user_pass)
#         self.assertTrue(user_superuser.is_staff)
#         self.assertTrue(user_superuser.is_superuser)

#     def test_user_str_representation(self):
#         '''
#         Create and test a new user and compare its email with str representation
#         '''
#         self.assertEqual(str(self.user_a), self.email)



#     def test_user_full_name(self):
#         self.assertEqual(self.user_a.get_full_name(), self.email)

#     def test_user_short_name(self):
#         self.assertEqual(self.user_a.get_short_name(), self.email)

