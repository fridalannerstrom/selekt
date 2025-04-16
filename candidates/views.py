from django.shortcuts import render, redirect
from .models import Candidate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})