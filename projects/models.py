from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms.models import model_to_dict


class Project(models.Model):
    class Etat(models.TextChoices):
        PLANIFICATION = "Planification", "Planification"
        EXECUTION = "Exécution", "Exécution"
        CLOTURE = "Clôturé", "Clôturé"

    reference = models.CharField(max_length=50, unique=True)
    intitule = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    etat = models.CharField(max_length=20, choices=Etat.choices, default=Etat.PLANIFICATION)
    budget_previsionnel = models.DecimalField(max_digits=14, decimal_places=2)
    montant_contrat = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    taux_avancement = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    date_debut = models.DateField()
    date_fin_prevue = models.DateField()
    archive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.reference} - {self.intitule}"

    @property
    def montant_contrat_affichage(self):
        if self.montant_contrat in (None, Decimal("0"), Decimal("0.00")):
            return ""
        return self.montant_contrat

    @property
    def situation_projet(self):
        if self.etat != self.Etat.EXECUTION:
            return ""
        return f"{self.taux_avancement}%"


class ProjectHistory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="historiques")
    champ_modifie = models.CharField(max_length=100)
    ancienne_valeur = models.TextField(blank=True)
    nouvelle_valeur = models.TextField(blank=True)
    date_modification = models.DateTimeField(auto_now_add=True)
    modifie_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="project_changes"
    )

    class Meta:
        ordering = ["-date_modification"]


TRACKED_FIELDS = [
    "reference",
    "intitule",
    "description",
    "etat",
    "budget_previsionnel",
    "montant_contrat",
    "taux_avancement",
    "date_debut",
    "date_fin_prevue",
    "archive",
]


def build_project_history(previous_project, updated_project, user=None):
    if previous_project is None:
        return

    before = model_to_dict(previous_project, fields=TRACKED_FIELDS)
    after = model_to_dict(updated_project, fields=TRACKED_FIELDS)

    for field in TRACKED_FIELDS:
        old_value = before.get(field)
        new_value = after.get(field)
        if old_value != new_value:
            ProjectHistory.objects.create(
                project=updated_project,
                champ_modifie=field,
                ancienne_valeur="" if old_value is None else str(old_value),
                nouvelle_valeur="" if new_value is None else str(new_value),
                modifie_par=user,
            )
