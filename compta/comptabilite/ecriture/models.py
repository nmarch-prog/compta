from django.db import models

# Create your models here.

class Compte(models.Model):

    nom = models.CharField(max_length=50)
    banque = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Ecriture(models.Model):

    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    date_operation = models.DateField()
    date_valeur = models.DateField()
    debit = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    credit = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    libelle = models.CharField(max_length=100)
    hors_compta = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date_operation) + ' - ' +self.libelle


