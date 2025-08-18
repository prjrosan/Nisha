from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_view_with_city_parameter(self):
        response = self.client.get(reverse('home') + '?city=Tokyo,Japan')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_view_context_contains_weather(self):
        response = self.client.get(reverse('home'))
        self.assertIn('weather', response.context)
        self.assertIsInstance(response.context['weather'], dict)
