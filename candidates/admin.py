from django.contrib import admin
from .models import Candidate, CandidateFile

# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job_title', 'location', 'uploaded_at')
    search_fields = ('name', 'email', 'top_skills')

@admin.register(CandidateFile)
class CandidateFileAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'file', 'uploaded_at')