from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = [
            'name', 'email', 'phone_number', 'job_title',
            'profile_summary', 'work_experience', 'education',
            'location', 'links', 'profile_image', 'other', 'notes', 'top_skills'
        ]
        widgets = {
            'profile_summary': forms.Textarea(attrs={'rows': 4}),
            'work_experience': forms.Textarea(attrs={'rows': 4}),
            'education': forms.Textarea(attrs={'rows': 4}),
            'other': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # All fields except 'name' are optional
        for field_name, field in self.fields.items():
            if field_name != 'name':
                field.required = False

            field.widget.attrs['class'] = 'form-control'


def get_links(form):
    """
    Return the links as a list of dictionaries: [{'name': ..., 'url': ...}]
    """
    links = []
    link_data = form.data.get('links') or form.initial.get('links')

    if link_data:
        link_items = link_data.split(';;;')
        for item in link_items:
            parts = item.split(':::')
            if len(parts) == 2:
                links.append({'name': parts[0], 'url': parts[1]})
    return links