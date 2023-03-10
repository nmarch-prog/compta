# Generated by Django 4.1.3 on 2023-02-17 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieComptable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=20)),
                ('no_compta', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('banque', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ecriture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_operation', models.DateField()),
                ('date_valeur', models.DateField()),
                ('debit', models.DecimalField(decimal_places=2, max_digits=8)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=8)),
                ('libelle', models.CharField(max_length=100)),
                ('hors_compta', models.BooleanField(default=False)),
                ('compte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comptabilite.compte')),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('emise', 'emise'), ('recue', 'recue')], max_length=10)),
                ('emetteur', models.CharField(max_length=50)),
                ('client', models.CharField(blank=True, max_length=50, null=True)),
                ('date_emission', models.DateField(blank=True, null=True)),
                ('fichier', models.FileField(blank=True, null=True, upload_to='')),
                ('future_facture', models.BooleanField(blank=True, null=True)),
                ('periodicite', models.CharField(choices=[('aucune', 'aucune'), ('mensuel', 'mensuel'), ('trimestriel', 'trimestriel')], default='aucune', max_length=50)),
                ('date_debut', models.DateField(blank=True, null=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('facture_liee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comptabilite.facture')),
            ],
        ),
        migrations.CreateModel(
            name='ElementComptable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField(blank=True, null=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comptabilite.categoriecomptable')),
                ('ecriture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comptabilite.ecriture')),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comptabilite.facture')),
            ],
        ),
        migrations.CreateModel(
            name='Echeance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_recouvrement', models.DateField()),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comptabilite.facture')),
            ],
        ),
    ]
