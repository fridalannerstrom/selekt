from django.db import models

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
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