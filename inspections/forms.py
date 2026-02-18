from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Inspection, InspectionType
from equipment.models import Equipment


class InspectionTypeForm(forms.ModelForm):
    class Meta:
        model = InspectionType
        fields = ['name', 'frequency', 'description', 'checklist']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Daily Inspection, Monthly Check'
            }),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description of the inspection type'
            }),
            'checklist': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Checklist items (one per line)'
            }),
        }
        labels = {
            'name': 'Inspection Type Name',
            'frequency': 'Frequency',
            'description': 'Description',
            'checklist': 'Checklist'
        }


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = [
            'equipment', 'inspection_type', 'inspection_date',
            'status', 'inspector_name',
            'findings', 'corrective_actions'
        ]
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-select'}),
            'inspection_type': forms.Select(attrs={'class': 'form-select'}),
            'inspection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'inspector_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inspector name'
            }),
            'findings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Inspection results and remarks'
            }),
            'corrective_actions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Corrective actions (if needed)'
            }),
        }
        labels = {
            'equipment': 'Equipment',
            'inspection_type': 'Inspection Type',
            'inspection_date': 'Inspection Date',
            'status': 'Status',
            'inspector_name': 'Inspector Name',
            'findings': 'Findings',
            'corrective_actions': 'Corrective Actions'
        }
        help_texts = {
            'inspection_date': 'Next inspection date will be calculated automatically'
        }

