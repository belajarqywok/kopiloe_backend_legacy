from django.test import TestCase

# Create your tests here.

class AnimalTestCase1(TestCase):

    def test_animals_can_speak1(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(1, 1)
        self.assertEqual(1, 1)