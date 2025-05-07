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

    def test_update_candidate(self):
        """User can update an existing candidate."""
        candidate = Candidate.objects.create(
            user=self.user,
            name='Old Name',
            email='old@example.com',
            job_title='Tester'
        )

        response = self.client.post(reverse('candidate_edit', args=[candidate.id]), {
            'name': 'New Name',
            'email': 'new@example.com',
            'job_title': 'Senior Tester',
            'top_skills': 'Testing, Python'
        })

        self.assertRedirects(response, reverse('candidate_edit', args=[candidate.id]))
        candidate.refresh_from_db()
        self.assertEqual(candidate.name, 'New Name')
        self.assertEqual(candidate.email, 'new@example.com')


    def test_delete_candidate(self):
        """User can delete their candidate."""
        candidate = Candidate.objects.create(user=self.user, name='Delete Me')

        response = self.client.post(reverse('candidate_delete', args=[candidate.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Candidate.objects.filter(id=candidate.id).exists())