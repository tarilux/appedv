from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    AdminLoginView,
    dashboard,
    export_excel,
    export_pdf,
    export_ppt,
    history_list,
    project_archive,
    project_create,
    project_detail,
    project_list,
    project_update,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", AdminLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("projects/", project_list, name="project_list"),
    path("projects/add/", project_create, name="project_create"),
    path("projects/<int:pk>/", project_detail, name="project_detail"),
    path("projects/<int:pk>/edit/", project_update, name="project_update"),
    path("projects/<int:pk>/archive/", project_archive, name="project_archive"),
    path("history/", history_list, name="history_list"),
    path("export/excel/", export_excel, name="export_excel"),
    path("export/pdf/<int:pk>/", export_pdf, name="export_pdf"),
    path("export/ppt/", export_ppt, name="export_ppt"),
]
