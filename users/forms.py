from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import UserProfile
from equipment.models import Department


class CustomUserCreationForm(UserCreationForm):
    """
    Custom registration form with additional fields
    """
    email = forms.EmailField(
        required=True,
        label='Имейл',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имейл адрес'
        }),
        help_text='Задължително. Въведете валиден имейл адрес.',
        error_messages={
            'required': 'Моля, въведете имейл адрес.',
            'invalid': 'Въведете валиден имейл адрес.'
        }
    )
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Име',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Име'
        }),
        error_messages={
            'required': 'Моля, въведете име.'
        }
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        }),
        error_messages={
            'required': 'Моля, въведете фамилия.'
        }
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+359888123456'
        }),
        help_text='Незадължително. Формат: +359888123456'
    )
    
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        label='Звено',
        empty_label="Избери звено",
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Незадължително. Изберете вашето звено.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': 'Потребителско име',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Потребителско име'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Потребителско име'
        self.fields['username'].help_text = 'Задължително. 150 символа или по-малко. Само букви, цифри и @/./+/-/_'
        self.fields['username'].error_messages = {
            'required': 'Моля, въведете потребителско име.',
            'unique': 'Потребител с това име вече съществува.'
        }
        
        self.fields['password1'].label = 'Парола'
        self.fields['password1'].help_text = 'Паролата трябва да съдържа поне 8 символа и да не е само цифри.'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Парола'
        })
        self.fields['password1'].error_messages = {
            'required': 'Моля, въведете парола.'
        }
        
        self.fields['password2'].label = 'Потвърди парола'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Потвърди парола'
        })
        self.fields['password2'].error_messages = {
            'required': 'Моля, потвърдете паролата.'
        }
    
    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Потребител с този имейл вече съществува.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Сигналът автоматично създава UserProfile
            # Сега само актуализираме допълнителните полета
            profile = user.profile  # Вече съществува заради сигнала
            profile.phone = self.cleaned_data.get('phone', '')
            profile.department = self.cleaned_data.get('department')
            profile.is_approved = False
            profile.save()

        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling (Bulgarian)
    Includes custom validation for unapproved users
    """
    username = forms.CharField(
        label='Потребителско име',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Въведете потребителско име',
            'autofocus': True
        }),
        error_messages={
            'required': 'Моля, въведете потребителско име.',
        }
    )
    password = forms.CharField(
        label='Парола',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Въведете парола'
        }),
        error_messages={
            'required': 'Моля, въведете парола.',
        }
    )
    
    error_messages = {
        'invalid_login': 'Моля, въведете правилно потребителско име и парола. '
                        'Обърнете внимание, че двете полета могат да са чувствителни към главни и малки букви.',
        'inactive': 'Този акаунт е неактивен.',
        'unapproved': 'Вашият акаунт е регистриран успешно, но все още чака одобрение от администратор. '
                     'Ще получите достъп след одобрението.',
    }
    
    def clean(self):
        """
        Custom validation to provide specific message for unapproved users
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username is not None and password:
            from django.contrib.auth import authenticate
            from django.contrib.auth.backends import ModelBackend
            
            backend = ModelBackend()
            user = backend.authenticate(self.request, username=username, password=password)
            
            if user is not None:
                if not user.is_superuser:
                    if hasattr(user, 'profile'):
                        if not user.profile.is_approved:
                            raise ValidationError(
                                self.error_messages['unapproved'],
                                code='unapproved',
                            )
                
                self.confirm_login_allowed(user)
                
                self.user_cache = user
            else:
                raise self.get_invalid_login_error()
        
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information
    """
    class Meta:
        model = UserProfile
        fields = ('phone', 'department', 'bio', 'avatar', 'birth_date', 'address', 'emergency_contact', 'certifications')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+359888123456'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Разкажете накратко за себе си...'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Вашият адрес'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Име и телефон за спешен контакт'
            }),
            'certifications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Списък със сертификати (по един на ред)'
            }),
        }

