from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile


class CustomLoginView(LoginView):
    """Custom Login View"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('equipment:dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Невалидно потребителско име или парола.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Custom Logout View"""
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Излязохте успешно от системата.')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """User Registration View"""
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Регистрацията е успешна! Моля изчакайте одобрение от администратор преди да можете да влезете.'
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Моля поправете грешките във формата.')
        return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    """User Profile View"""
    model = UserProfile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit User Profile"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Профилът беше обновен успешно!')
        return super().form_valid(form)


# Backwards compatibility
login_view = CustomLoginView.as_view()
logout_view = CustomLogoutView.as_view()
register_view = RegisterView.as_view()
profile_view = ProfileView.as_view()
profile_edit_view = ProfileEditView.as_view()

