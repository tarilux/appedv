import re

from django import forms
from .models import Project


SOUS_ETAPES_PAR_ETAPE = {
    'CP': ['DT'],
    'ISE': ['Validation ISE', 'Lancement AO', 'AO Publié', 'Evaluation technique', 'Validation de l\'ET', 'OC', 'CAD', 'OTP', 'Contrat'],
    'Exécution': ['Kick-off & OS', 'Livraison', 'Travaux en cours', 'WO'],
    'NA': ['NA'],
    'Annulé': ['Annulé'],
}

SITUATION_OPTIONS = [
    'Clôturé',
    'Encours',
    'OS signé : En Préparation pour début Travaux',
    'Contracté',
    'Attente OS',
    'Attente contrat',
    'En difficulté',
]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'id_projet', 'type', 'exercice', 'etape_en_cours', 'sous_etape', 'libelle', 'chef_projet',
            'montant_estime', 'montant_engage', 'num_contrat', 'montant_contrat', 'fournisseur',
            'date_signature_os', 'delai_projet', 'date_fin_contrat', 'date_fin_actualisee', 'autonomie',
            'total_attachement', 'dernier_mois_attache', 'avancement_travaux', 'travaux_precedents',
            'travaux_en_cours', 'travaux_prochains', 'situation_projet'
        ]
        widgets = {
            'date_signature_os': forms.DateInput(attrs={'type': 'date'}),
            'travaux_precedents': forms.Textarea(attrs={'rows': 3}),
            'travaux_en_cours': forms.Textarea(attrs={'rows': 3}),
            'travaux_prochains': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        etape = cleaned_data.get('etape_en_cours')
        sous_etape = cleaned_data.get('sous_etape')
        situation = cleaned_data.get('situation_projet')

        if etape:
            allowed = SOUS_ETAPES_PAR_ETAPE.get(etape, [])
            if sous_etape not in allowed:
                self.add_error('sous_etape', f'Sous-étape invalide pour {etape}. Valeurs autorisées: {", ".join(allowed)}')

        if etape == 'Exécution':
            if situation and situation not in SITUATION_OPTIONS:
                self.add_error('situation_projet', 'Situation projet invalide pour Exécution.')
        else:
            cleaned_data['situation_projet'] = None

        mm_yyyy_regex = re.compile(r'^(0[1-9]|1[0-2])/\d{4}$')
        for field in ['date_fin_contrat', 'date_fin_actualisee', 'dernier_mois_attache']:
            value = cleaned_data.get(field)
            if value and not mm_yyyy_regex.match(value):
                self.add_error(field, 'Format attendu: MM/YYYY')

        return cleaned_data
