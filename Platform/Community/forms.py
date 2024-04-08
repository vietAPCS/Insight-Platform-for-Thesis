from django import forms
from .models import *

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ('name', 'created_user', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'created_user': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }