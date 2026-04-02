from django import forms
from django.core.exceptions import ValidationError
from .models import Equipment, EquipmentCategory, Manufacturer, Department, Location, Technician


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'country', 'website', 'contact_info']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mettler Toledo, Sartorius'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Germany, USA'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'contact_info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Информация за контакт'
            }),
        }
        labels = {
            'name': 'Име на производител',
            'country': 'Държава',
            'website': 'Уебсайт',
            'contact_info': 'Информация за контакт'
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'asset_number', 'name', 'category', 'manufacturer',
            'model', 'serial_number', 'location', 'location_old', 'commissioning_date',
            'requires_oq_pv', 'requires_calibration', 'requires_technical_review',
            'check_interval_months', 'notes'
        ]
        widgets = {
            'asset_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'например: EQ-001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име на оборудването'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Модел'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сериен номер'
            }),
            'location': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location_old': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Локация (старо поле, скоро ще бъде премахнато)',
                'readonly': 'readonly'
            }),
            'commissioning_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'requires_oq_pv': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'requires_calibration': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'requires_technical_review': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'check_interval_months': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Допълнителни бележки'
            }),
        }
        labels = {
            'asset_number': 'ASSET номер',
            'name': 'Наименование',
            'category': 'Категория',
            'manufacturer': 'Производител',
            'model': 'Модел',
            'serial_number': 'Сериен номер',
            'location': 'Локация',
            'location_old': 'Локация (старо поле - за справка)',
            'commissioning_date': 'Дата на въвеждане в експлоатация',
            'requires_oq_pv': 'Изисква OQ/PV',
            'requires_calibration': 'Изисква калибровка',
            'requires_technical_review': 'Изисква технически преглед',
            'check_interval_months': 'Периодичност на проверки',
            'notes': 'Бележки'
        }
        help_texts = {
            'requires_oq_pv': 'Подлежи на OQ/PV валидиране',
            'requires_calibration': 'Подлежи на калибровка (везни, pH метри)',
            'requires_technical_review': 'Подлежи на технически преглед',
        }

    def clean_asset_number(self):
        asset_number = self.cleaned_data.get('asset_number')
        if asset_number:
            asset_number = asset_number.upper()
            if self.instance.pk:
                if Equipment.objects.exclude(pk=self.instance.pk).filter(
                    asset_number=asset_number
                ).exists():
                    raise ValidationError('ASSET номерът вече съществува.')
        return asset_number

    def clean_serial_number(self):
        serial_number = self.cleaned_data.get('serial_number')
        if self.instance.pk:
            if Equipment.objects.exclude(pk=self.instance.pk).filter(
                serial_number=serial_number
            ).exists():
                raise ValidationError('Серийният номер вече съществува.')
        return serial_number


class EquipmentCategoryForm(forms.ModelForm):
    class Meta:
        model = EquipmentCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'например: pH метър, Спектрофотометър, Везна'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание на категорията'
            }),
        }
        labels = {
            'name': 'Име на категория',
            'description': 'Описание'
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['code', 'name', 'full_name', 'manager', 'contact', 'is_active']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ККП, КИОМ и т.н.'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кратко име на звеното'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пълно наименование на звеното'
            }),
            'manager': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име на ръководител'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон, email и т.н.'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'code': 'Код на звено',
            'name': 'Наименование',
            'full_name': 'Пълно наименование',
            'manager': 'Ръководител',
            'contact': 'Контакт',
            'is_active': 'Активно'
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'category', 'floor', 'room_number', 'name', 'department',
            'building', 'area_sqm', 'responsible_person', 'phone',
            'has_controlled_temperature', 'has_controlled_humidity',
            'notes', 'is_active'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1, 2, 3...'
            }),
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '102, 205...'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Лаборатория ККП'
            }),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'building': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сграда А, Главна сграда...'
            }),
            'area_sqm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Площ в кв.м',
                'step': '0.01'
            }),
            'responsible_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име на отговорното лице'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон'
            }),
            'has_controlled_temperature': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'has_controlled_humidity': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Допълнителни бележки'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'category': 'Категория',
            'floor': 'Етаж',
            'room_number': 'Номер на помещение',
            'name': 'Име на лаборатория/помещение',
            'department': 'Звено',
            'building': 'Сграда',
            'area_sqm': 'Площ (кв.м)',
            'responsible_person': 'Отговорно лице',
            'phone': 'Телефон',
            'has_controlled_temperature': 'Контролирана температура',
            'has_controlled_humidity': 'Контролирана влажност',
            'notes': 'Забележки',
            'is_active': 'Активна'
        }
        help_texts = {
            'category': 'Категория на помещението (A, B, C, D, E)',
            'floor': 'Номер на етаж',
            'room_number': 'Номер на помещението',
        }


class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = [
            'user', 'first_name', 'last_name', 'position', 'specialization',
            'phone', 'email', 'department', 'company',
            'certification', 'certification_expiry', 'notes', 'is_active'
        ]
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-select',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Длъжност'
            }),
            'specialization': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Външна фирма (незадължително)'
            }),
            'certification': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Сертификати и квалификации'
            }),
            'certification_expiry': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Допълнителни бележки'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'user': 'Свързан потребител',
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'position': 'Длъжност',
            'specialization': 'Специализация',
            'phone': 'Телефон',
            'email': 'Email',
            'department': 'Звено',
            'company': 'Външна фирма',
            'certification': 'Сертификати',
            'certification_expiry': 'Валидност на сертификат до',
            'notes': 'Забележки',
            'is_active': 'Активен'
        }
        help_texts = {
            'user': 'Изберете потребител от системата (само за вътрешни техници). За външни техници оставете празно.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показване само на потребители с роля "technician" които нямат Technician профил
        from django.contrib.auth.models import User

        # Филтриране на потребители
        technician_users = User.objects.filter(
            profile__role='technician',
            profile__is_approved=True
        )

        # Ако редактираме съществуващ техник, включи текущия потребител
        if self.instance.pk and self.instance.user:
            technician_users = technician_users | User.objects.filter(pk=self.instance.user.pk)
        else:
            # Изключи потребители, които вече имат Technician профил
            technician_users = technician_users.exclude(technician_profile__isnull=False)

        self.fields['user'].queryset = technician_users
        self.fields['user'].empty_label = "--- Без потребител (външен техник) ---"
