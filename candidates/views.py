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
from django.db.models import Q, Count


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required
def dashboard(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    filter_title = request.GET.get('title', '')  # 👈 NYTT!

    candidates = Candidate.objects.filter(user=request.user)
    candidates = filter_candidates(candidates, query)

    # Filter
    if filter_title:
        candidates = candidates.filter(job_title__iexact=filter_title)

    # Sorting
    if sort == 'name':
        candidates = candidates.order_by('name')
    else:
        candidates = candidates.order_by('-uploaded_at')

    # Top 6 jobbtitles
    job_titles = (
        Candidate.objects
        .filter(user=request.user)
        .exclude(job_title__isnull=True)
        .exclude(job_title__exact='')
        .values('job_title')
        .annotate(count=Count('job_title'))
        .order_by('-count')[:6]
    )
    for candidate in candidates:
        candidate.skill_list = [skill.strip() for skill in candidate.top_skills.split(',')]

    context = {
        'candidates': candidates,
        'job_titles': job_titles,
        'active_title': filter_title, 
    }
    return render(request, 'dashboard.html', context)

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


# Candidate Search
def candidate_search(request):
    query = request.GET.get('q', '')
    candidates = Candidate.objects.all()
    candidates = filter_candidates(candidates, query)

    return render(request, 'candidate-search.html', {'candidates': candidates})

def filter_candidates(queryset, query):
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(job_title__icontains=query) |
            Q(location__icontains=query) |
            Q(top_skills__icontains=query)
        )
    return queryset