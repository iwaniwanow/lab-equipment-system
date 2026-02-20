from django import forms
from django.core.exceptions import ValidationError
from .models import Equipment, EquipmentCategory, Manufacturer


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
                'placeholder': 'Contact information'
            }),
        }
        labels = {
            'name': 'Manufacturer Name',
            'country': 'Country',
            'website': 'Website',
            'contact_info': 'Contact Information'
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'asset_number', 'name', 'category', 'manufacturer',
            'model', 'serial_number', 'location', 'commissioning_date',
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
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Локация в лабораторията'
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
                    raise ValidationError('ASSET number already exists.')
        return asset_number

    def clean_serial_number(self):
        serial_number = self.cleaned_data.get('serial_number')
        if self.instance.pk:
            if Equipment.objects.exclude(pk=self.instance.pk).filter(
                serial_number=serial_number
            ).exists():
                raise ValidationError('Serial number already exists.')
        return serial_number


class EquipmentCategoryForm(forms.ModelForm):
    class Meta:
        model = EquipmentCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., pH meter, Spectrophotometer, Balance'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description'
            }),
        }
        labels = {
            'name': 'Category Name',
            'description': 'Description'
        }
