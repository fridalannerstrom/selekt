"""
URL configuration for cleoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from candidates import views as candidate_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from candidates import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('signup/', candidate_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard & home
    path('', candidate_views.index, name='index'),
    path('dashboard/', candidate_views.dashboard, name='dashboard'),

    # App: Candidates
    path('candidates/', include('candidates.urls')),

    # User settings & account
    path('settings/', views.settings_view, name='settings'),
    path('settings/delete/', views.delete_account, name='delete_account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)