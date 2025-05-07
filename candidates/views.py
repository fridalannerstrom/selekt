# ==========================================
# IMPORTS
# ==========================================

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import FormView
from django.urls import reverse
from django.utils.http import urlencode

import fitz  # PyMuPDF
import logging
import json
import os
import env

from openai import OpenAI
from .models import Candidate, CandidateFile, Profile, Favorite
from .forms import CandidateForm

logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# ==========================================
# BASIC VIEWS: Index, Dashboard, Signup
# ==========================================


# View for the landing page. Redirects logged-in users to dashboard.
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')


# Handles dashboard logic: filtering, sorting, pagination and favorites.
@login_required
def dashboard(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    filter_title = request.GET.get('title', '')
    show_favorites = request.GET.get('favorites') == 'on'

    candidates = Candidate.objects.filter(user=request.user)
    candidates = filter_candidates(candidates, query)

    # Filter
    if filter_title:
        candidates = candidates.filter(job_title__iexact=filter_title)

    # Favorites
    if show_favorites:
        favorite_candidates = Favorite.objects.filter(user=request.user).values_list('candidate_id', flat=True)
        candidates = candidates.filter(id__in=favorite_candidates)

    # Sorting
    if sort == 'name':
        candidates = candidates.order_by('name')
    else:
        candidates = candidates.order_by('-uploaded_at')

    # Top 5 jobbtitles
    job_titles = (
        Candidate.objects
        .filter(user=request.user)
        .exclude(job_title__isnull=True)
        .exclude(job_title__exact='')
        .values('job_title')
        .annotate(count=Count('job_title'))
        .order_by('-count')[:4]
    )

    # Pagination
    paginator = Paginator(candidates, 12)
    page_number = request.GET.get('page')
    candidates = paginator.get_page(page_number)

    # Prepare skill list and favorites
    for candidate in candidates:
        candidate.skill_list = [skill.strip() for skill in candidate.top_skills.split(',')]
        candidate.is_favorite = Favorite.objects.filter(user=request.user, candidate=candidate).exists()

    # Show welcome popup for first-time users
    show_welcome_popup = False
    if hasattr(request.user, 'profile') and request.user.profile.is_first_login:
        show_welcome_popup = True

    context = {
        'candidates': candidates,
        'job_titles': job_titles,
        'active_title': filter_title, 
        'show_favorites': show_favorites,
        'show_welcome_popup': show_welcome_popup,
    }
    return render(request, 'dashboard.html', context)


# Signup view using built-in UserCreationForm
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

# ==========================================
# CANDIDATE VIEWS: Create, Read, Update, Delete, Modal, File Upload
# ==========================================

# Create new candidate (standard form)
@method_decorator(login_required, name='dispatch')
class CandidateCreateView(CreateView):
    model = Candidate
    form_class = CandidateForm
    template_name = 'candidate-form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Format custom links
        link_names = self.request.POST.getlist('link_names')
        link_urls = self.request.POST.getlist('link_urls')
        combined_links = ''
        for name, url in zip(link_names, link_urls):
            if name and url:
                combined_links += f'{name}:::{url};;;'
        form.instance.links = combined_links

        response = super().form_valid(form)

        # Handle file uploads
        for file in self.request.FILES.getlist('candidate_files'):
            CandidateFile.objects.create(candidate=self.object, file=file)

        return response

    def get_success_url(self):
        return reverse_lazy('dashboard')


# Candidate detail view
class CandidateDetailView(DetailView):
    model = Candidate
    template_name = 'candidate-detail.html'
    context_object_name = 'candidate'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("This candidate does not belong to you.")
        return obj

# Update candidate
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

        # Reformat links
        link_names = self.request.POST.getlist('link_names')
        link_urls = self.request.POST.getlist('link_urls')

        combined_links = ''
        for name, url in zip(link_names, link_urls):
            if name and url:
                combined_links += f'{name}:::{url};;;'

        self.object.links = combined_links
        self.object.save()

        messages.success(self.request, mark_safe('Candidate is updated'))
        return response    

    def get_success_url(self):
        return self.request.path


# Load candidate modal (AJAX)
@login_required
def candidate_modal(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk, user=request.user)
    skills = [skill.strip() for skill in candidate.top_skills.split(',')] if candidate.top_skills else []
    candidate.skill_list = skills 

    candidate.is_favorite = Favorite.objects.filter(user=request.user, candidate=candidate).exists()
  
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

# Upload files to existing candidate
def upload_candidate_files(request, pk):
    candidate = get_object_or_404(Candidate, id=pk)

    if request.method == 'POST':
        for file in request.FILES.getlist('files'):
            CandidateFile.objects.create(candidate=candidate, file=file)
        return JsonResponse({'message': 'Files uploaded successfully'})

    return JsonResponse({'error': 'Only POST method allowed'}, status=400)



# Get files for candidate
@login_required
def get_candidate_files(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk, user=request.user)
    html = render_to_string('file-list.html', {'candidate': candidate})
    return JsonResponse({'html': html})

# Delete single file
@login_required
def delete_candidate_file(request, file_id):
    candidate_file = get_object_or_404(CandidateFile, id=file_id, candidate__user=request.user)
    candidate_file.delete()
    return JsonResponse({'message': 'File deleted successfully'})


# Candidate search view
def candidate_search(request):
    query = request.GET.get('q', '')
    candidates = Candidate.objects.all()
    candidates = filter_candidates(candidates, query)

    return render(request, 'candidate-search.html', {'candidates': candidates})

# Filtering
def filter_candidates(queryset, query):
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(job_title__icontains=query) |
            Q(location__icontains=query) |
            Q(top_skills__icontains=query)
        )
    return queryset


# ==========================================
# FAVORITE & WELCOME LOGIC
# ==========================================


# Toggle favorite status for candidate
@csrf_exempt
@login_required
def toggle_favorite(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, candidate=candidate)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})

# Dismiss welcome popup
@csrf_exempt
@login_required
def dismiss_welcome(request):
    if request.method == 'POST':
        if hasattr(request.user, 'profile'):
            request.user.profile.is_first_login = False
            request.user.profile.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


# ==========================================
# ACCOUNT & SETTINGS
# ==========================================

# Delete user account
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request) 
        user.delete()   
        return redirect('index')  
    else:
        return redirect('settings')


# View and update user settings (name, email, password, profile picture)
@login_required
def settings_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')

        if 'profile_picture' in request.FILES:
            profile.profile_image = request.FILES['profile_picture']

        # Password change validation        
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if current_password or new_password1 or new_password2:
            if not current_password or not new_password1 or not new_password2:
                messages.error(request, 'To change your password, you must fill in all three fields.')
                return redirect('settings')

            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('settings')

            if new_password1 != new_password2:
                messages.error(request, 'New passwords do not match.')
                return redirect('settings')

            try:
                validate_password(new_password1, user=user)
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
                return redirect('settings')

            user.set_password(new_password1)
            update_session_auth_hash(request, user)  # så att man inte loggas ut
            messages.success(request, 'Your password has been changed successfully.')


        user.save()
        profile.save()

        messages.success(request, 'Your settings have been updated successfully!')
        return redirect('settings')

    return render(request, 'settings.html', {'user': user, 'profile': profile})


# ==========================================
# AI PDF HANDLING (OpenAI, CV parsing)
# ==========================================


# Upload PDF file and parse it with OpenAI
@login_required
def upload_pdf_candidates(request):
    if request.method == 'GET':
        return render(request, 'upload-candidate.html')

    elif request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        try:
            text = extract_text_from_pdf(file)
            structured_data = call_openai(text)
            result = {
                'status': 'success',
                'filename': file.name,
                'text': text,
                'structured': structured_data
            }
        except Exception as e:
            logger.error(f"OpenAI or parsing error: {e}")
            return JsonResponse({
                'results': [{
                    'status': 'error',
                    'filename': file.name,
                    'error': "Something went wrong while analyzing the CV. Please try again with another file."
                }]
            }, status=500)

        return JsonResponse({'results': [result]})


# Extract text from uploaded PDF
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


# Call OpenAI to extract structured data from CV text
def call_openai(text):
    prompt = f"""
    You are an expert AI recruiter. Your task is to extract structured candidate data from the following CV text. 
    Please return a JSON object in this format:

    {{
        "name": "",
        "email": "",
        "phone_number": "",
        "job_title": "",       # Suggest a relevant title if not clearly stated. Make it short and relevant. Do not use & or "and" in title.
        "profile_summary": "", # Write a short professional summary based on the CV content
        "work_experience": "",
        "education": "",
        "location": "",
        "links": "",
        "top_skills": "",      
        # Only return short, keyword-style skills as a comma-separated string.
        Prioritize the shortest and most relevant terms first (e.g. “SQL, Python, UX”).
        Avoid full sentences or descriptive phrases.
        "other": "",
        "notes": ""
    }}

    CV text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)

# Save parsed data temporarily in session
@login_required
@require_http_methods(["POST"])
def create_candidate_from_openai(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    request.session['prefill_candidate'] = data
    return JsonResponse({'redirect_url': reverse('candidate_create_with_prefill')})

# Prefilled candidate creation view
class CandidateCreatePrefilledView(CreateView):
    model = Candidate
    form_class = CandidateForm
    template_name = 'candidate-form.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('prefill_candidate'):
            messages.success(request, "Information extracted from your PDF. Remember to save your candidate.")
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        data = self.request.session.get('prefill_candidate', {})
        for field in data:
            if field in initial:
                initial[field] = data[field]
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        link_names = self.request.POST.getlist('link_names')
        link_urls = self.request.POST.getlist('link_urls')
        combined_links = ''
        for name, url in zip(link_names, link_urls):
            if name and url:
                combined_links += f'{name}:::{url};;;'
        form.instance.links = combined_links

        response = super().form_valid(form)

        for file in self.request.FILES.getlist('candidate_files'):
            CandidateFile.objects.create(candidate=self.object, file=file)

        return response

    def get_success_url(self):
        return reverse_lazy('dashboard')