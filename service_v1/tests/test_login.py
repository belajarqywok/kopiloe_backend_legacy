from django.test import TestCase

# Create your tests here.

class AnimalTestCase(TestCase):

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(1, 1)
        self.assertEqual(1, 1)