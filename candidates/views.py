from django.shortcuts import render, redirect
from .models import Candidate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CandidateForm

# Create your views here.
def candidate_list(request):
    candidates = Candidate.objects.all().order_by('-uploaded_at')
    return render(request, 'candidate_list.html', {'candidates': candidates})

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    candidates = Candidate.objects.all().order_by('-uploaded_at')[:5]  # senaste 5
    return render(request, 'dashboard.html', {'candidates': Candidate.objects.all()})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)  
            candidate.user = request.user        
            candidate.save()                    
            return redirect('dashboard')
    else:
        form = CandidateForm()
    return render(request, 'add-candidate.html', {'form': form})