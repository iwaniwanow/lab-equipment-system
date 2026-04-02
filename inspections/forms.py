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

    def __init__(self, *args, **kwargs):
        # Вземаме текущия потребител от kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # САМО ЗА TECHNICIAN роля - автоматичен извършител и филтриране
        # OPERATOR може да избира извършител и вижда всички типове
        if user and hasattr(user, 'profile') and user.profile.role == 'technician':
            # Техникът трябва да има technician_profile
            if hasattr(user, 'technician_profile'):
                # Задаваме началната стойност да е техника
                if not self.instance.pk:  # Само при създаване
                    self.initial['technician'] = user.technician_profile

                # Правим полето само за четене
                self.fields['technician'].disabled = True
                self.fields['technician'].widget.attrs['readonly'] = 'readonly'
                self.fields['technician'].help_text = 'Вие сте автоматично зададен като извършител'

                # Филтриране на типове проверки според звеното на техника
                tech_profile = user.technician_profile
                if tech_profile.department:
                    dept_code = tech_profile.department.code.upper()

                    # Определяме позволените категории според звеното
                    allowed_categories = []
                    
                    # Технически отдел (ТО) → Технически прегледи
                    if dept_code == 'ТО':
                        allowed_categories = ['technical_review']
                        print(f"DEBUG Inspections: Технически отдел (ТО) - Технически прегледи")

                    # Лаборатории и контрол → Проверки за пригодност
                    # ККП, КИОМ, НР, ОК, КК, ФХК
                    elif dept_code in ['ККП', 'КИОМ', 'НР', 'ОК', 'КК', 'ФХК']:
                        allowed_categories = ['suitability_check']
                        print(f"DEBUG Inspections: Лаборатория/Контрол ({dept_code}) - Проверки за пригодност")

                    # Ако има определени категории, филтрираме
                    if allowed_categories:
                        from .models import InspectionType
                        filtered_queryset = InspectionType.objects.filter(category__in=allowed_categories)
                        print(f"DEBUG Inspections: Филтрирани типове: {list(filtered_queryset.values_list('name', flat=True))}")
                        self.fields['inspection_type'].queryset = filtered_queryset
                        self.fields['inspection_type'].help_text = f'Показани са само проверките, подходящи за звено {tech_profile.department.full_name or tech_profile.department.name}'
                    else:
                        print(f"DEBUG Inspections: Звено {dept_code} не е в списъка, показваме всички типове")

        # OPERATOR, ADMIN, MANAGER - без ограничения, виждат всички типове и могат да избират извършител

        # OPERATOR, ADMIN, MANAGER - без ограничения, виждат всички типове и могат да избират извършител



