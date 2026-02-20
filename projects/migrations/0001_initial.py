from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_projet', models.CharField(max_length=100, unique=True)),
                ('type', models.CharField(choices=[('GT', 'GT'), ('IV', 'IV')], max_length=2)),
                ('exercice', models.CharField(choices=[('Nouvelle Inscription', 'Nouvelle Inscription'), ('Engagement Antérieur', 'Engagement Antérieur')], max_length=30)),
                ('etape_en_cours', models.CharField(choices=[('CP', 'CP'), ('ISE', 'ISE'), ('Exécution', 'Exécution'), ('NA', 'NA'), ('Annulé', 'Annulé')], max_length=15)),
                ('sous_etape', models.CharField(max_length=255)),
                ('libelle', models.CharField(max_length=255)),
                ('chef_projet', models.CharField(max_length=120)),
                ('montant_estime', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('montant_engage', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('num_contrat', models.CharField(max_length=120)),
                ('montant_contrat', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('fournisseur', models.CharField(max_length=255)),
                ('date_signature_os', models.DateField(blank=True, null=True)),
                ('delai_projet', models.IntegerField(default=0)),
                ('date_fin_contrat', models.CharField(help_text='Format MM/YYYY', max_length=7)),
                ('date_fin_actualisee', models.CharField(help_text='Format MM/YYYY', max_length=7)),
                ('autonomie', models.IntegerField(default=0)),
                ('total_attachement', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('dernier_mois_attache', models.CharField(help_text='Format MM/YYYY', max_length=7)),
                ('avancement_travaux', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('travaux_precedents', models.TextField(blank=True)),
                ('travaux_en_cours', models.TextField(blank=True)),
                ('travaux_prochains', models.TextField(blank=True)),
                ('situation_projet', models.CharField(blank=True, max_length=255, null=True)),
                ('statut', models.CharField(choices=[('actif', 'actif'), ('archive', 'archive')], default='actif', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'db_table': 'projets'},
        ),
        migrations.CreateModel(
            name='HistoriqueModification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('champ_modifie', models.CharField(max_length=120)),
                ('ancienne_valeur', models.TextField(blank=True, null=True)),
                ('nouvelle_valeur', models.TextField(blank=True, null=True)),
                ('date_modification', models.DateTimeField(auto_now_add=True)),
                ('projet', models.ForeignKey(db_column='projet_id', on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={'db_table': 'historique_modifications', 'ordering': ['-date_modification']},
        ),
    ]
