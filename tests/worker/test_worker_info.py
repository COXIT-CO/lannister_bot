from django.test import TestCase
from lannister_auth .models import LannisterUser



class LannisterUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        LannisterUser.objects.create(username="alex", first_name='Oleksandr', last_name='Nykolyak')

    def test_title_content(self):
        lannisteruser = LannisterUser.objects.get(id=1)
        expected_object_name = f'{lannisteruser.username}'
        self.assertEquals(expected_object_name, 'alex')

    def test_body_content(self):
        lannisteruser = LannisterUser.objects.get(id=1)
        expected_object_name = f'{lannisteruser.first_name}'
        self.assertEquals(expected_object_name, 'Oleksandr')


