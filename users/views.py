from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, UserProfileUpdateForm, CustomAuthenticationForm, UserUpdateForm
from .models import UserProfile


class CustomLoginView(LoginView):
    """Custom Login View with Bulgarian form and approval check"""
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('equipment:dashboard')

    def form_invalid(self, form):
        """Handle form validation errors with appropriate messages"""
        # The form already contains the appropriate error message
        # No need to add additional messages here
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Custom Logout View - accepts GET requests"""
    next_page = reverse_lazy('users:login')
    http_method_names = ['get', 'post', 'options']  # Разрешава GET заявки

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.request.user  # Добавяне на user обект
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit User Profile with both User and UserProfile forms"""
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Rename form to profile_form for clarity
        context['profile_form'] = context['form']

        # Add user_form for User model fields
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        # Validate both forms
        if user_form.is_valid():
            user_form.save()
            messages.success(self.request, 'Профилът беше обновен успешно!')
            return super().form_valid(form)
        else:
            # If user_form is invalid, return with errors
            return self.form_invalid(form)


# Backwards compatibility
login_view = CustomLoginView.as_view()
logout_view = CustomLogoutView.as_view()
register_view = RegisterView.as_view()
profile_view = ProfileView.as_view()
profile_edit_view = ProfileEditView.as_view()

