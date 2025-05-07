from django.urls import path
from .views import (
    home, ProjectListView, ProjectDetailView, ProjectCreateView,
    ProjectUpdateView, ProjectDeleteView, register_view, login_view,
    logout_view, profile_view, contact_view
)

urlpatterns = [
    path('/', home, name='home'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/new/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<slug:slug>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<slug:slug>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('contact/', contact_view, name='contact'),
]
