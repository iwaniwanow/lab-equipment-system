from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, UserProfileUpdateForm
from .models import UserProfile


class RegisterView(CreateView):
    """
    User registration view (CBV)
    """
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Акаунт създаден успешно за {form.cleaned_data["username"]}! Моля изчакайте одобрение от администратор преди да влезете.')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('equipment:dashboard')
        return super().dispatch(request, *args, **kwargs)


def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('equipment:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if user is approved
                profile = UserProfile.objects.filter(user=user).first()
                if profile and not profile.is_approved:
                    messages.error(request, 'Вашият акаунт все още не е одобрен от администратор. Моля изчакайте одобрение.')
                    return redirect('users:login')
                
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'equipment:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('users:login')


class ProfileView(LoginRequiredMixin, DetailView):
    """
    User profile view (CBV)
    """
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self, queryset=None):
        return self.request.user


@login_required
def profile_edit_view(request):
    """
    Edit user profile view
    """
    user = request.user
    
    # Ensure user has a profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'users/profile_edit.html', context)


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    View for viewing other users' public profiles
    """
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
