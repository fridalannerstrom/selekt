from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Candidate
from django.conf import settings
from unittest.mock import patch, MagicMock
import json
from candidates.views import call_openai


class OpenAITests(TestCase):
    @patch('candidates.views.client.chat.completions.create')
    def test_call_openai_returns_expected_data(self, mock_create):
        """call_openai() should return structured JSON when OpenAI responds"""
        # Arrange
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content=json.dumps({
                "name": "Test Person",
                "email": "test@example.com",
                "phone_number": "123456789",
                "job_title": "Developer",
                "profile_summary": "An experienced developer.",
                "work_experience": "5 years at Company X",
                "education": "B.Sc. Computer Science",
                "location": "Stockholm",
                "links": "LinkedIn:::https://linkedin.com/in/test;;;",
                "top_skills": "Python, Django",
                "other": "",
                "notes": ""
            })))
        ]
        mock_create.return_value = mock_response

        # Act
        result = call_openai("Fake CV text here")

        # Assert
        self.assertEqual(result["name"], "Test Person")
        self.assertEqual(result["job_title"], "Developer")
        self.assertIn("Python", result["top_skills"])       

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
        response = self.client.post(reverse('candidates:candidate_add'), {
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

        response = self.client.post(reverse('candidates:candidate_edit', args=[candidate.id]), {
            'name': 'New Name',
            'email': 'new@example.com',
            'job_title': 'Senior Tester',
            'top_skills': 'Testing, Python'
        })

        self.assertRedirects(response, reverse('candidates:candidate_edit', args=[candidate.id]))
        candidate.refresh_from_db()
        self.assertEqual(candidate.name, 'New Name')
        self.assertEqual(candidate.email, 'new@example.com')


    def test_delete_candidate(self):
        """User can delete their candidate."""
        candidate = Candidate.objects.create(user=self.user, name='Delete Me')

        response = self.client.post(reverse('candidates:candidate_delete', args=[candidate.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Candidate.objects.filter(id=candidate.id).exists())

    def test_user_cannot_access_others_candidate(self):
        """Users should not be able to access another user's candidate detail view."""
        other_user = User.objects.create_user(username='otheruser', password='secret')
        candidate = Candidate.objects.create(user=other_user, name='Not Yours')

        response = self.client.get(reverse('candidates:candidate_detail', args=[candidate.id]))

        self.assertEqual(response.status_code, 404)

    def test_toggle_favorite(self):
        """User can toggle favorite status for a candidate."""
        candidate = Candidate.objects.create(user=self.user, name='Favorite Test')

        url = reverse('candidates:toggle_favorite', args=[candidate.id])
        
        # First POST – adds favorite
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'is_favorite': True})

        # Second POST – removes favorite
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'is_favorite': False})

    def test_candidate_create_form_prefills_from_session(self):
        """Candidate form should prefill from session data"""
        # Arrange
        session = self.client.session
        session['prefill_candidate'] = {
            'name': 'Session Test',
            'email': 'session@example.com',
            'job_title': 'Prefilled Role',
            'top_skills': 'React, Vue',
        }
        session.save()

        # Act
        response = self.client.get(reverse('candidates:candidate_create_with_prefill'))

        # Assert
        self.assertContains(response, 'value="Session Test"')
        self.assertContains(response, 'value="session@example.com"')
        self.assertContains(response, 'value="Prefilled Role"')
        self.assertContains(response, 'React, Vue')

    def test_welcome_modal_shown_only_once(self):
        """Welcome modal should appear only once for first-time users."""

        self.user.profile.is_first_login = True
        self.user.profile.save()

        # First visit: modal should be shown
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'id="welcomeModal"') 

        # Simulate dismissing the welcome popup via AJAX POST
        url = reverse('candidates:dismiss_welcome')
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        # Refresh profile and check that the first login flag is now False
        self.user.profile.refresh_from_db()
        self.assertFalse(self.user.profile.is_first_login)

        # Second visit: modal should no longer be shown
        response = self.client.get(reverse('dashboard'))
        self.assertNotContains(response, 'id="welcomeModal"')