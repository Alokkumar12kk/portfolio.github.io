from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from .models import Project, Profile, Skill
from .forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm, ProjectForm


def home(request):
    featured_projects = Project.objects.filter(featured=True)[:3]
    skills = Skill.objects.all()
    return render(request, 'portfolio_app/index.html', {
        'featured_projects': featured_projects,
        'skills': skills
    })


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio_app/project_list.html'
    context_object_name = 'projects'
    paginate_by = 6
    ordering = ['-date_created']


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio_app/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_projects'] = Project.objects.exclude(pk=self.object.pk).filter(
            technologies__in=self.object.technologies.all()).distinct()[:3]
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio_app/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio_app/project_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'portfolio_app/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'portfolio_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)
            messages.success(request, 'Logged in successfully!')
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'portfolio_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    projects = Project.objects.filter(user=request.user)
    return render(request, 'portfolio_app/profile.html', {
        'form': form,
        'projects': projects,
    })


def contact_view(request):
    if request.method == 'POST':
        messages.success(request, 'Your message has been sent!')
        return redirect('contact')
    return render(request, 'portfolio_app/contact.html')


def custom_404(request, exception):
    return render(request, 'portfolio_app/404.html', status=404)
