from django.contrib import admin
from django.urls import path
from projects import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.projects_page, name='projects_page'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/archive/', views.project_archive, name='project_archive'),
    path('projects/<int:pk>/restore/', views.project_restore, name='project_restore'),
    path('archive/', views.archive_list, name='archive_list'),
    path('history/', views.history_list, name='history_list'),
    path('export/projects.xlsx', views.export_xlsx, name='export_xlsx'),
    path('export/projects.pdf', views.export_pdf, name='export_pdf'),
    path('export/projects.pptx', views.export_pptx, name='export_pptx'),
]
