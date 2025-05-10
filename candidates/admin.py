from django.contrib import admin
from .models import Candidate, CandidateFile, Profile, Favorite


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job_title', 'location', 'uploaded_at')
    search_fields = ('name', 'email', 'top_skills')


@admin.register(CandidateFile)
class CandidateFileAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'file', 'uploaded_at')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_first_login')
    search_fields = ('user__username',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate')
    search_fields = ('user__username', 'candidate__name')
