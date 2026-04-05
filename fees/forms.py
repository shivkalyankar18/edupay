from django import forms
from .models import Fee
from django.utils import timezone

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ('student', 'course', 'amount', 'due_date', 'status')
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }