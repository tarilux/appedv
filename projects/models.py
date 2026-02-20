import json
from decimal import Decimal, ROUND_HALF_UP

from django.db import models


class Project(models.Model):
    TYPE_CHOICES = [('GT', 'GT'), ('IV', 'IV')]
    EXERCICE_CHOICES = [
        ('Nouvelle Inscription', 'Nouvelle Inscription'),
        ('Engagement Antérieur', 'Engagement Antérieur'),
    ]
    ETAPE_CHOICES = [
        ('CP', 'CP'),
        ('ISE', 'ISE'),
        ('Exécution', 'Exécution'),
        ('NA', 'NA'),
        ('Annulé', 'Annulé'),
    ]
    STATUT_CHOICES = [('actif', 'actif'), ('archive', 'archive')]

    id_projet = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    exercice = models.CharField(max_length=30, choices=EXERCICE_CHOICES)
    etape_en_cours = models.CharField(max_length=15, choices=ETAPE_CHOICES)
    sous_etape = models.CharField(max_length=255)
    libelle = models.CharField(max_length=255)
    chef_projet = models.CharField(max_length=120)
    montant_estime = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    montant_engage = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    num_contrat = models.CharField(max_length=120)
    montant_contrat = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    fournisseur = models.CharField(max_length=255)
    date_signature_os = models.DateField(null=True, blank=True)
    delai_projet = models.IntegerField(default=0)
    date_fin_contrat = models.CharField(max_length=7, help_text='Format MM/YYYY')
    date_fin_actualisee = models.CharField(max_length=7, help_text='Format MM/YYYY')
    autonomie = models.IntegerField(default=0)
    total_attachement = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    dernier_mois_attache = models.CharField(max_length=7, help_text='Format MM/YYYY')
    avancement_travaux = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    travaux_precedents = models.TextField(blank=True)
    travaux_en_cours = models.TextField(blank=True)
    travaux_prochains = models.TextField(blank=True)
    situation_projet = models.CharField(max_length=255, null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projets'

    @property
    def pourcentage_reception(self):
        if self.montant_contrat <= 0:
            return None
        value = (self.total_attachement / self.montant_contrat) * Decimal('100')
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f'{self.id_projet} - {self.libelle}'

    def snapshot(self):
        payload = {
            'id_projet': self.id_projet,
            'type': self.type,
            'exercice': self.exercice,
            'etape_en_cours': self.etape_en_cours,
            'sous_etape': self.sous_etape,
            'libelle': self.libelle,
            'chef_projet': self.chef_projet,
            'montant_estime': str(self.montant_estime),
            'montant_engage': str(self.montant_engage),
            'num_contrat': self.num_contrat,
            'montant_contrat': str(self.montant_contrat),
            'fournisseur': self.fournisseur,
            'date_signature_os': self.date_signature_os.isoformat() if self.date_signature_os else None,
            'delai_projet': self.delai_projet,
            'date_fin_contrat': self.date_fin_contrat,
            'date_fin_actualisee': self.date_fin_actualisee,
            'autonomie': self.autonomie,
            'total_attachement': str(self.total_attachement),
            'pourcentage_reception': str(self.pourcentage_reception) if self.pourcentage_reception is not None else None,
            'dernier_mois_attache': self.dernier_mois_attache,
            'avancement_travaux': str(self.avancement_travaux),
            'travaux_precedents': self.travaux_precedents,
            'travaux_en_cours': self.travaux_en_cours,
            'travaux_prochains': self.travaux_prochains,
            'situation_projet': self.situation_projet,
            'statut': self.statut,
        }
        return json.dumps(payload, ensure_ascii=False)


class HistoriqueModification(models.Model):
    projet = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='projet_id')
    champ_modifie = models.CharField(max_length=120)
    ancienne_valeur = models.TextField(null=True, blank=True)
    nouvelle_valeur = models.TextField(null=True, blank=True)
    date_modification = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historique_modifications'
        ordering = ['-date_modification']
