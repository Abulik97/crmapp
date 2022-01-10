from django.urls import reverse
from django.test import TestCase

# Create your tests here.

class TestLandingPage(TestCase):
    def status_code(self):
        response=self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'landing.html')
        print(response.status_code)
