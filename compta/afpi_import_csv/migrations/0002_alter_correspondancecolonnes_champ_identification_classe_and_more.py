# Generated by Django 4.1.3 on 2022-12-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afpi_import_csv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correspondancecolonnes',
            name='champ_identification_classe',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='correspondancecolonnes',
            name='classe_liee',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
