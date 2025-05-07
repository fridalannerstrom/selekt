from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Candidate
from django.conf import settings

class CandidateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_dashboard_loads(self):
        """Dashboard should return 200 for logged in user."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_create_candidate(self):
        """User can create a candidate."""
        response = self.client.post(reverse('candidate_add'), {
            'name': 'Anna Test',
            'email': 'anna@example.com',
            'job_title': 'Developer',
            'top_skills': 'Python, Django',
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(Candidate.objects.filter(name='Anna Test').exists())

    def test_dashboard_requires_login(self):
        """Dashboard should redirect unauthenticated users."""
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        expected_redirect = f"{settings.LOGIN_URL}?next={reverse('dashboard')}"
        self.assertRedirects(response, expected_redirect)

