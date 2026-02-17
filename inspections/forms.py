from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Inspection, InspectionType
from equipment.models import Equipment


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = [
            'equipment', 'inspection_type', 'inspection_date',
            'next_inspection_date', 'status', 'inspector_name',
            'findings', 'corrective_actions'
        ]
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-select'}),
            'inspection_type': forms.Select(attrs={'class': 'form-select'}),
            'inspection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'next_inspection_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'readonly': 'readonly'  # Read-only поле
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'inspector_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име на инспектора'
            }),
            'findings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Резултати и забележки от проверката'
            }),
            'corrective_actions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Коригиращи действия (при нужда)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Автоматично изчисление на следваща дата
        if not self.instance.pk and 'inspection_date' in self.initial:
            inspection_date = self.initial['inspection_date']
            inspection_type = self.initial.get('inspection_type')
            if inspection_type:
                self.fields['next_inspection_date'].initial = self._calculate_next_date(
                    inspection_date, inspection_type
                )

    def _calculate_next_date(self, inspection_date, inspection_type):
        frequency_map = {
            'daily': 1,
            'weekly': 7,
            'monthly': 30,
            'quarterly': 90,
            'biannual': 180,
            'annual': 365,
        }
        days = frequency_map.get(inspection_type.frequency, 30)
        return inspection_date + timedelta(days=days)

    def clean(self):
        cleaned_data = super().clean()
        inspection_date = cleaned_data.get('inspection_date')
        next_inspection_date = cleaned_data.get('next_inspection_date')

        if inspection_date and next_inspection_date:
            if next_inspection_date <= inspection_date:
                raise forms.ValidationError(
                    'Следващата дата на проверка трябва да е след текущата!'
                )

        return cleaned_data


class InspectionTypeForm(forms.ModelForm):
    class Meta:
        model = InspectionType
        fields = ['name', 'frequency', 'description', 'checklist']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Напр. Дневна проверка'
            }),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'checklist': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Списък с проверки (на нов ред)'
            }),
        }
