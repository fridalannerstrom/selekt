from django.urls import path
from . import views


urlpatterns = [
    path('', views.CandidateListView.as_view(), name='candidate_list'), # Lista alla kandidater
    path('add/', views.CandidateCreateView.as_view(), name='candidate_add'),  # Lägg till kandidat
    path('<int:pk>/', views.CandidateDetailView.as_view(), name='candidate_detail'),  # Se profil
    path('<int:pk>/edit/', views.CandidateUpdateView.as_view(), name='candidate_edit'),  # Redigera kandidat
    path('candidate-modal/<int:pk>/', views.candidate_modal, name='candidate_modal'),
    path('<int:pk>/delete/', views.CandidateDeleteView.as_view(), name='candidate_delete'),
]