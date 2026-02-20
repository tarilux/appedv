# Application interne de suivi des projets (Django)

Application web interne moderne type ERP pour le suivi administratif, financier et opérationnel des projets.

## Stack technique adoptée

- **Backend** : Django
- **Base relationnelle** : PostgreSQL ou MySQL (configurable via variables d'environnement)
- **Frontend** : Bootstrap 5 + design ERP responsive
- **Graphiques** : Chart.js
- **Exports** :
  - Excel : données brutes filtrées
  - PDF : rapport synthèse (KPI + sections graphiques + tableau synthèse)
  - PowerPoint : slide dashboard + graphiques + tableau synthèse

## Structure base de données

### Table `projets`

Implémentée via le modèle `Project` avec les champs:

- `id`, `id_projet`, `type`, `exercice`, `etape_en_cours`, `sous_etape`
- `libelle`, `chef_projet`, `montant_estime`, `montant_engage`
- `num_contrat`, `montant_contrat`, `fournisseur`, `date_signature_os`, `delai_projet`
- `date_fin_contrat`, `date_fin_actualisee`, `autonomie`, `total_attachement`
- `dernier_mois_attache`, `avancement_travaux`
- `travaux_precedents`, `travaux_en_cours`, `travaux_prochains`, `situation_projet`
- `statut` (`actif`/`archive`), `created_at`, `updated_at`

`pourcentage_reception` est calculé automatiquement et non éditable:

- si `montant_contrat > 0` → `(total_attachement / montant_contrat) * 100` (arrondi 2 décimales)
- sinon → `null`

### Table `historique_modifications`

- `id`
- `projet_id`
- `champ_modifie`
- `ancienne_valeur`
- `nouvelle_valeur`
- `date_modification`

Chaque changement de champ est enregistré (création, modification, archivage, restauration).

## Règles métier implémentées

1. **Sous-étapes conditionnelles** en fonction de `etape_en_cours` (validées côté serveur + UI dynamique).
2. **Situation Projet** affichée uniquement pour `Exécution`, sinon masquée et forcée à `null`.
3. **Archivage logique** : pas de suppression physique, bouton Archiver, invisibles par défaut, filtre d’affichage des archivés.
4. **Historique des modifications** champ-par-champ.

5. **Page Projets interactive** : tri colonnes, pagination, recherche globale, filtres (type, exercice, étape, sous-étape, chef, autonomie, situation) et code couleur du % réception.

## Lancer localement

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Puis ouvrir `http://localhost:8000`.
