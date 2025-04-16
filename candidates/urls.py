from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidate_list, name='candidate_list'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
]