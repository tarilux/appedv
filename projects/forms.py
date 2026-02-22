from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "reference",
            "intitule",
            "description",
            "etat",
            "budget_previsionnel",
            "montant_contrat",
            "taux_avancement",
            "date_debut",
            "date_fin_prevue",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "date_debut": forms.DateInput(attrs={"type": "date"}),
            "date_fin_prevue": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin_prevue = cleaned_data.get("date_fin_prevue")
        if date_debut and date_fin_prevue and date_fin_prevue < date_debut:
            self.add_error("date_fin_prevue", "La date de fin prévue doit être postérieure à la date de début.")
        return cleaned_data
