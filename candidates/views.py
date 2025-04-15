from django.shortcuts import render
from .models import Candidate

# Create your views here.
def candidate_list(request):
    candidates = Candidate.objects.all().order_by('-uploaded_at')
    return render(request, 'candidate_list.html', {'candidates': candidates})

def index(request):
    return render(request, 'index.html')