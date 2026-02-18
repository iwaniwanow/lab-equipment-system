from django import forms
from .models import MaintenanceRecord, MaintenanceType


class MaintenanceTypeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceType
        fields = ['name', 'type', 'period_months', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Annual Calibration, OQ/PV'
            }),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'period_months': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '12 (for annual), 6 (for semi-annual)',
                'min': 1
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description of the maintenance type'
            }),
        }
        labels = {
            'name': 'Maintenance Type Name',
            'type': 'Type',
            'period_months': 'Period (Months)',
            'description': 'Description'
        }


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'equipment', 'maintenance_type', 'performed_date',
            'next_due_date', 'performed_by', 'certificate_number',
            'results', 'cost', 'notes'
        ]
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-select'}),
            'maintenance_type': forms.Select(attrs={'class': 'form-select'}),
            'performed_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'next_due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'readonly': 'readonly'
            }),
            'performed_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Department (Metrology/QC) or name'
            }),
            'certificate_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certificate/Protocol number'
            }),
            'results': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Calibration/Validation results'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cost (optional)',
                'step': '0.01'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes'
            }),
        }
        labels = {
            'equipment': 'Equipment',
            'maintenance_type': 'Maintenance Type',
            'performed_date': 'Performed Date',
            'next_due_date': 'Next Due Date',
            'performed_by': 'Performed By',
            'certificate_number': 'Certificate Number',
            'results': 'Results',
            'cost': 'Cost',
            'notes': 'Notes'
        }
        help_texts = {
            'performed_date': 'Enter the date when maintenance was performed',
            'next_due_date': 'Auto-calculated based on maintenance type period (read-only)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make next_due_date field not required - it will be auto-calculated
        self.fields['next_due_date'].required = False
