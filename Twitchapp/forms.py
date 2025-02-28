from django.forms import ModelForm
from .models import Profile
from django import forms
from .models import TwitchPost


class ProfileForm(ModelForm):
    class Meta:

        model = Profile
        fields = ['icon', 'status_message']
class TwitchPostForm(forms.ModelForm):
    class Meta:
        model = TwitchPost
        fields = ['movie_title', 'content', 'category', 'movie']
        widgets = {
            'movie_title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'movie': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
