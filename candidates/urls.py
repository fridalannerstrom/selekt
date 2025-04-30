from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.CandidateCreateView.as_view(), name='candidate_add'), 
    path('<int:pk>/', views.CandidateDetailView.as_view(), name='candidate_detail'),  
    path('<int:pk>/edit/', views.CandidateUpdateView.as_view(), name='candidate_edit'),
    path('candidate-modal/<int:pk>/', views.candidate_modal, name='candidate_modal'),
    path('<int:pk>/delete/', views.CandidateDeleteView.as_view(), name='candidate_delete'),
    path('<int:pk>/upload-files/', views.upload_candidate_files, name='upload_candidate_files'),
    path('<int:pk>/files/', views.get_candidate_files, name='get_candidate_files'),
    path('file/<int:file_id>/delete/', views.delete_candidate_file, name='delete_candidate_file'),
    path('candidates/search/', views.candidate_search, name='candidate_search'),
    path('upload/', views.upload_pdf_candidates, name='upload_pdf_candidates'),
]