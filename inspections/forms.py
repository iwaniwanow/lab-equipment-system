from django import forms
from .models import Inspection, InspectionType
from equipment.models import Equipment


class InspectionTypeForm(forms.ModelForm):
    class Meta:
        model = InspectionType
        fields = ['name', 'category', 'frequency', 'description', 'checklist']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'например: Дневна проверка, Месечен контрол'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание на типа проверка'
            }),
            'checklist': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Списък с проверки (по една на ред)'
            }),
        }
        labels = {
            'name': 'Наименование',
            'category': 'Категория',
            'frequency': 'Честота',
            'description': 'Описание',
            'checklist': 'Контролен списък'
        }


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = [
            'equipment', 'inspection_type', 'inspection_date',
            'status', 'technician',
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
            'technician': forms.Select(attrs={'class': 'form-select'}),
            'findings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Констатации и резултати от проверката'
            }),
            'corrective_actions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Коригиращи действия (ако са необходими)'
            }),
        }
        labels = {
            'equipment': 'Оборудване',
            'inspection_type': 'Тип проверка',
            'inspection_date': 'Дата на проверка',
            'status': 'Статус',
            'technician': 'Техник/Изпълнител',
            'findings': 'Констатации',
            'corrective_actions': 'Коригиращи действия'
        }
        help_texts = {
            'inspection_date': 'Следващата дата на проверка ще бъде изчислена автоматично',
            'technician': 'Изберете техник от списъка'
        }



