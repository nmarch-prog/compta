from django.db import models

# Create your models here.

class Facture(models.Model):

    type = models.CharField(max_length=10, choices=[('emise', 'emise'), ('recue', 'recue')])
    emetteur = models.CharField(max_length=50)
    client = models.CharField(max_length=50, null=True, blank=True)
    date_emission = models.DateField(null=True, blank=True)
    fichier = models.FileField(null=True, blank=True)
    #commercial = models.CharField(max_length=20, null=True, blank=True)
    #apporteur = models.CharField(max_length=20, null=True, blank=True)
    #retrocession_commercial = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    #date_retro_commercial = models.DateField(null=True, blank=True)
    #retrocession_apporteur = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    #date_retro_apporteur = models.DateField(null=True, blank=True)
    future_facture = models.BooleanField(null=True, blank=True)
    client = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.date_emission) + ' - ' + self.emetteur



class Echeance(models.Model):
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    date_recouvrement = models.DateField()
    facture = models.ForeignKey(Facture, null=True, blank=True, on_delete=models.CASCADE)
