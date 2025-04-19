from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, CreateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Candidate
from .forms import CandidateForm
from django.http import Http404

# Index
def index(request):
    return render(request, 'index.html')

# Dashboard
@login_required
def dashboard(request):
    candidates = Candidate.objects.filter(user=request.user).order_by('-uploaded_at')[:5]
    return render(request, 'dashboard.html', {'candidates': candidates})

# Signup
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

# Candidate list
class CandidateListView(ListView):
    model = Candidate
    template_name = 'candidate-list.html'
    context_object_name = 'candidates'

    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user).order_by('-uploaded_at')

# Add candidate
@method_decorator(login_required, name='dispatch')
class CandidateCreateView(CreateView):
    model = Candidate
    form_class = CandidateForm
    template_name = 'candidate-form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')

# Candidate detail
class CandidateDetailView(DetailView):
    model = Candidate
    template_name = 'candidate-detail.html'
    context_object_name = 'candidate'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("This candidate does not belong to you.")
        return obj

# Edit candidate
class CandidateUpdateView(UpdateView):
    model = Candidate
    fields = ['name', 'email', 'top_skills', 'notes']
    template_name = 'candidate-form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("This candidate does not belong to you.")
        return obj    

    def get_success_url(self):
        return reverse_lazy('candidate_detail', kwargs={'pk': self.object.pk})