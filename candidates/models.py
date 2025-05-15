from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage

# ==========================
# Main Candidate Model
# ==========================


class Candidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    profile_summary = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    links = models.CharField(max_length=255, blank=True,
                             help_text="e.g. LinkedIn, GitHub URLs")
    profile_image = CloudinaryField('image', blank=True, null=True)
    other = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    top_skills = models.CharField(
        blank=True,
        help_text="Write top skills separated by commas "
        "(e.g. Communication, Leadership, SQL)"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def skill_list(self):
        """
        Returns the 'top_skills' field as a clean list.
        """
        return [skill.strip()
                for skill in self.top_skills.split(",") if skill.strip()]

    def get_links(self):
        """
        Converts the serialized 'links'
        string (format: name:::url;;;name:::url)
        into a list of dictionaries for easier use in templates.
        """
        if not self.links:
            return []
        parts = self.links.split(';;;')
        links = []
        for part in parts:
            if ':::' in part:
                name, url = part.split(':::', 1)
                links.append({'name': name, 'url': url})
        return links

# ==========================
# Files uploaded per Candidate
# ==========================


class CandidateFile(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(
        upload_to='candidate_files/',
        storage=RawMediaCloudinaryStorage()
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


# ==========================
# Extended User Profile
# ==========================

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', blank=True, null=True)
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# Automatically create or update Profile when a User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# ==========================
# Favorite Candidates
# ==========================


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ('user', 'candidate')  # Prevent duplicate favorites

    def __str__(self):
        return f"{self.user.username} ❤️ {self.candidate.name}"
