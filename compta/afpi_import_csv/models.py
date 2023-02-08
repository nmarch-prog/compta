from django.db import models

# Create your models here.

class TypeFichier(models.Model):

    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class CorrespondanceColonnes(models.Model):

    type_fich = models.ForeignKey(TypeFichier, on_delete=models.CASCADE)
    colonne_initiale = models.CharField(max_length=50)
    champ_cible = models.CharField(max_length=50)
    # les colonnes qui seront verfiees pour les écritures en double sont à "True"
    flag_doublon = models.BooleanField()
    flag_foreignkey = models.BooleanField()
    classe_liee = models.CharField(max_length=50,null=True, blank=True)
    champ_identification_classe = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.type_fich) + ' - ' + str(self.champ_cible)


class FormatCsv(models.Model):

    type_fich = models.OneToOneField(TypeFichier, on_delete=models.CASCADE)
    csv_line_separator = models.CharField(max_length=5)
    csv_field_separator = models.CharField(max_length=1)
    csv_encoding = models.CharField(max_length=15)
    decimal_separator = models.CharField(max_length=1)
    date_format = models.CharField(max_length=10)

    def __str__(self):
        return self.type_fich.nom

