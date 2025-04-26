from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Candidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    profile_summary = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    links = models.CharField(max_length=255, blank=True, help_text="e.g. LinkedIn, GitHub URLs")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    other = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    top_skills = models.CharField(
        max_length=255,
        blank=True,
        help_text="Write top skills separated by commas (e.g. Communication, Leadership, SQL)"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def skill_list(self):
        return [skill.strip() for skill in self.top_skills.split(",") if skill.strip()]