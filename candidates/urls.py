from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidate_list, name='candidate_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]