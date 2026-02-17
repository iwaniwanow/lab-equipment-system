from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import MaintenanceRecord, MaintenanceType


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
                'readonly': 'readonly'  # Read-only
            }),
            'performed_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отдел Метрологичен/КИП или име'
            }),
            'certificate_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер на сертификат/протокол'
            }),
            'results': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Резултати от калибрирането/валидацията'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена (опционално)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Допълнителни бележки'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Автоматично изчисление на следваща дата (годишно за калибрирания)
        if not self.instance.pk:
            self.fields['next_due_date'].initial = timezone.now().date() + timedelta(days=365)

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if cost and cost < 0:
            raise forms.ValidationError('Цената не може да е отрицателна.')
        return cost

    def clean(self):
        cleaned_data = super().clean()
        performed_date = cleaned_data.get('performed_date')
        next_due_date = cleaned_data.get('next_due_date')

        if performed_date and next_due_date:
            if next_due_date <= performed_date:
                raise forms.ValidationError(
                    'Следващата дата на поддръжка трябва да е след текущата!'
                )

        return cleaned_data


class MaintenanceTypeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceType
        fields = ['name', 'type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Напр. Годишна калибрация'
            }),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
