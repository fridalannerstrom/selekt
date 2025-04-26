from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Candidate, CandidateFile
from .forms import CandidateForm
from django.http import Http404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.template import RequestContext


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

# Dashboard
@login_required
def dashboard(request):
    candidates = Candidate.objects.filter(user=request.user).order_by('-uploaded_at')[:5]

    for candidate in candidates:
        # Dela upp strängen till en lista, t.ex. "HTML, CSS" → ["HTML", "CSS"]
        candidate.skill_list = [skill.strip() for skill in candidate.top_skills.split(',')]

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
    fields = [
            'name', 'email', 'phone_number', 'job_title', 'profile_summary',
            'work_experience', 'education', 'location', 'links',
            'profile_image', 'other', 'notes', 'top_skills'
        ]
    template_name = 'candidate-form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("This candidate does not belong to you.")
        return obj    
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, mark_safe('Candidate is updated'))
        return response    

    def get_success_url(self):
        return self.request.path
    

# Candidate Modal
@login_required
def candidate_modal(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk, user=request.user)
    skills = [skill.strip() for skill in candidate.top_skills.split(',')] if candidate.top_skills else []
    candidate.skill_list = skills  # Lägg till för att kunna loopa

    html = render_to_string('candidate-modal.html', {'candidate': candidate}, request=request)
    return JsonResponse({'html': html})

# Delete candidate
class CandidateDeleteView(DeleteView):
    model = Candidate
    template_name = 'candidate-confirm-delete.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("This candidate does not belong to you.")
        return obj

def upload_candidate_files(request, pk):
    candidate = get_object_or_404(Candidate, id=pk)

    if request.method == 'POST':
        for file in request.FILES.getlist('files'):
            CandidateFile.objects.create(candidate=candidate, file=file)
        return JsonResponse({'message': 'Files uploaded successfully'})

    return JsonResponse({'error': 'Only POST method allowed'}, status=400)

@login_required
def get_candidate_files(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk, user=request.user)
    html = render_to_string('file-list.html', {'candidate': candidate})
    return JsonResponse({'html': html})


@login_required
def delete_candidate_file(request, file_id):
    candidate_file = get_object_or_404(CandidateFile, id=file_id, candidate__user=request.user)
    candidate_file.delete()
    return JsonResponse({'message': 'File deleted successfully'})