from django.urls import path
from . import views
from .views import CandidateDetailView, CandidateUpdateView, CandidateCreateView, CandidateListView

urlpatterns = [
    path('', views.CandidateListView.as_view(), name='candidate_list'), # Lista alla kandidater
    path('add/', views.CandidateCreateView.as_view(), name='candidate_add'),  # Lägg till kandidat
    path('<int:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),  # Se profil
    path('<int:pk>/edit/', CandidateUpdateView.as_view(), name='candidate_edit'),  # Redigera kandidat
]