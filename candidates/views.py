from django.shortcuts import render
from .models import Candidate
from django.contrib.auth.decorators import login_required

# Create your views here.
def candidate_list(request):
    candidates = Candidate.objects.all().order_by('-uploaded_at')
    return render(request, 'candidate_list.html', {'candidates': candidates})

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    candidates = Candidate.objects.all().order_by('-uploaded_at')[:5]  # senaste 5
    return render(request, 'dashboard.html', {'candidates': Candidate.objects.all()})