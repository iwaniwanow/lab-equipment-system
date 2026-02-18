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
            'model', 'serial_number', 'location', 'required_maintenance_types',
            'purchase_date', 'notes'
        ]
        widgets = {
            'asset_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., EQ-001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Equipment name'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Serial number'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Laboratory location'
            }),
            'required_maintenance_types': forms.CheckboxSelectMultiple(),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes'
            }),
        }
        labels = {
            'asset_number': 'ASSET Number',
            'name': 'Equipment Name',
            'category': 'Category',
            'manufacturer': 'Manufacturer',
            'model': 'Model',
            'serial_number': 'Serial Number',
            'location': 'Location',
            'required_maintenance_types': 'Required Maintenance Types',
            'purchase_date': 'Purchase Date',
            'notes': 'Notes'
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
