from tkinter.font import names

from django.urls import path

from . import views
from . import api_views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('projects/<slug:slug>/edit/', views.ProjectUpdateView.as_view(), name="project-edit"),
    path('projects/<slug:slug>/delete/', views.ProjectDeleteView.as_view(), name="project-delete"),
    path('materials/', views.MaterialListView.as_view(), name="materials"),
    path('materials/new/', views.MaterialCreateView.as_view(), name='material-create'),
    path('materials/<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material-edit'),
    path('materials/<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material-delete'),
    path('daily-logs/', views.DailyLogListView.as_view(), name='daily_logs'),
    path('daily-logs/new/', views.DailyLogCreateView.as_view(), name="daily_log-create"),
    path('daily-logs/<int:pk>/edit/', views.DailyLogUpdateView.as_view(), name="daily_log-edit"),
    path('daily-logs/<int:pk>/delete/', views.DailyLogDeleteView.as_view(), name="daily_log-delete"),
    path('api/projects/', api_views.ProjectListApiView.as_view(), name="projects-api"),
    path('api/projects/<int:pk>/', api_views.ProjectDetailApiView.as_view(), name="project-api"),
    path('api/materials/', api_views.MaterialListApiView.as_view(), name="materials-api"),
    path('api/materials/<int:pk>/', api_views.MaterialDetailApiView.as_view(), name="material-api"),
]
