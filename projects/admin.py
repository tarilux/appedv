from django.contrib import admin

from .models import Project, ProjectHistory


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("reference", "intitule", "etat", "budget_previsionnel", "montant_contrat", "archive")
    search_fields = ("reference", "intitule")
    list_filter = ("etat", "archive")


@admin.register(ProjectHistory)
class ProjectHistoryAdmin(admin.ModelAdmin):
    list_display = ("project", "champ_modifie", "date_modification", "modifie_par")
    search_fields = ("project__reference", "champ_modifie")
