from django.urls import path
from . import views
from candidates import views as candidate_views

urlpatterns = [
    path('', views.candidate_list, name='candidate_list'),
    path('add/', candidate_views.add_candidate, name='add_candidate'),
]