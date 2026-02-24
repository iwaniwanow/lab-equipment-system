from django import forms
from .models import MaintenanceRecord, MaintenanceType


class MaintenanceTypeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceType
        fields = ['name', 'type', 'period_months', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'например: Годишна калибровка, OQ/PV'
            }),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'period_months': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '12 (за годишна), 6 (за шестмесечна)',
                'min': 1
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание на типа поддръжка'
            }),
        }
        labels = {
            'name': 'Наименование',
            'type': 'Тип',
            'period_months': 'Период (месеци)',
            'description': 'Описание'
        }


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'equipment', 'maintenance_type', 'performed_date',
            'next_due_date', 'technician', 'certificate_number',
            'result', 'work_performed', 'parts_used', 'cost', 'currency', 'notes'
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
            'technician': forms.Select(attrs={'class': 'form-select'}),
            'certificate_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер на сертификат/протокол'
            }),
            'result': forms.Select(attrs={'class': 'form-select'}),
            'work_performed': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Извършени дейности и резултати'
            }),
            'parts_used': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Използвани части/материали (ако има)'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена (незадължително)',
                'step': '0.01'
            }),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Допълнителни бележки'
            }),
        }
        labels = {
            'equipment': 'Оборудване',
            'maintenance_type': 'Тип поддръжка',
            'performed_date': 'Дата на изпълнение',
            'next_due_date': 'Следваща дата',
            'technician': 'Техник/Изпълнител',
            'certificate_number': 'Номер на сертификат',
            'result': 'Резултат',
            'work_performed': 'Извършена работа',
            'parts_used': 'Използвани части',
            'cost': 'Цена',
            'currency': 'Валута',
            'notes': 'Бележки'
        }
        help_texts = {
            'performed_date': 'Въведете датата на изпълнение',
            'next_due_date': 'Автоматично изчислена въз основа на периода (само за четене)',
            'technician': 'Изберете техник от списъка',
            'parts_used': 'Незадължително - списък с части или материали'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['next_due_date'].required = False
        self.fields['parts_used'].required = False
