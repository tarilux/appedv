# PROtrack

Application web Django pour le suivi de projets administratifs, financiers et opérationnels.

## Stack technique
- Backend: Django
- Base de données: PostgreSQL (ou SQLite local par défaut)
- Frontend: HTML5/CSS3, Bootstrap 5, Vanilla JS
- Graphiques: Chart.js
- Exports: openpyxl (Excel), reportlab (PDF), python-pptx (PowerPoint)

## Installation
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## PostgreSQL
Configurer les variables suivantes pour activer PostgreSQL:

```bash
export DB_ENGINE=postgres
export POSTGRES_DB=protrack
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

## Migrations
```bash
python manage.py makemigrations projects
python manage.py migrate
```

## Fonctionnalités
- Dashboard KPI + charts (doughnut et courbe budget)
- CRUD projet (sans suppression, archivage uniquement)
- Historisation automatique des modifications
- Recherche dynamique + pagination
- Exports Excel, PDF, PPT
- Authentification admin
- Pages d'erreur personnalisées (404/500)
