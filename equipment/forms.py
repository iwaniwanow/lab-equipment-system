from django import forms
from django.core.exceptions import ValidationError
from .models import Equipment, EquipmentCategory


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'asset_number', 'name', 'category', 'manufacturer',
            'model', 'serial_number', 'location', 'status',
            'purchase_date', 'notes'
        ]
        widgets = {
            'asset_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Напр. EQ-001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име на оборудването'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Производител'
            }),
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
            'status': forms.Select(attrs={'class': 'form-select'}),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Допълнителни бележки'
            }),
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
                raise ValidationError('Сериен номер вече съществува.')
        return serial_number


class EquipmentCategoryForm(forms.ModelForm):
    class Meta:
        model = EquipmentCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Напр. pH метър, спектрофотометър'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание на категорията'
            }),
        }
