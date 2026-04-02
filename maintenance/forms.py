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
        # Вземаме текущия потребител от kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['next_due_date'].required = False
        self.fields['parts_used'].required = False
        
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
                
                # Филтриране на типове поддръжка според звеното на техника
                tech_profile = user.technician_profile
                if tech_profile.department:
                    dept_code = tech_profile.department.code.upper()
                    dept_full_name = tech_profile.department.full_name.lower() if tech_profile.department.full_name else ''

                    # Определяме позволените типове според звеното
                    allowed_types = []
                    
                    # Метрологичен отдел (МО) → Калибровки
                    if dept_code == 'МО':
                        allowed_types = ['calibration']
                        print(f"DEBUG: Метрологичен отдел (МО) - Калибровки")

                    # Технически отдел (ТО) → Ремонт и Технически преглед
                    elif dept_code == 'ТО':
                        allowed_types = ['repair', 'technical_service']
                        print(f"DEBUG: Технически отдел (ТО) - Ремонт и Технически преглед")

                    # Лаборатории, Качествен контрол, Наука и развитие
                    # ККП, КИОМ, НР, ОК, КК, ФХК → Валидиране
                    elif dept_code in ['ККП', 'КИОМ', 'НР', 'ОК', 'КК', 'ФХК']:
                        allowed_types = ['validation']
                        print(f"DEBUG: Лаборатория/Контрол ({dept_code}) - Валидиране")

                    # Ако има определени типове, филтрираме
                    if allowed_types:
                        from .models import MaintenanceType
                        filtered_queryset = MaintenanceType.objects.filter(type__in=allowed_types)
                        print(f"DEBUG: Филтрирани типове: {list(filtered_queryset.values_list('name', flat=True))}")
                        self.fields['maintenance_type'].queryset = filtered_queryset
                        self.fields['maintenance_type'].help_text = f'Показани са само типовете, подходящи за звено {tech_profile.department.full_name or tech_profile.department.name}'
                    else:
                        print(f"DEBUG: ВНИМАНИЕ - Звено {dept_code} не е в списъка, показваме всички типове")
