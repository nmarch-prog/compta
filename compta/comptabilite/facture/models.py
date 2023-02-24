from django.db import models

# Create your models here.

class Facture(models.Model):

    type = models.CharField(max_length=10, choices=[('emise', 'emise'), ('recue', 'recue')])
    emetteur = models.CharField(max_length=50)
    # Si la facture est liée à un client d'AFPI
    client = models.CharField(max_length=50, null=True, blank=True)
    date_emission = models.DateField(null=True, blank=True)
    fichier = models.FileField(null=True, blank=True)
    # Facture n'ayant pas en entrer en comptabilité (service non encore fourni)
    # Pour les échéancier, une échéance rentrerea en compta avec les ecritures des comptes
    future_facture = models.BooleanField(null=True, blank=True)
    # Si la facture dépend d'une autre, par exemple com apporteur
    facture_liee = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    # Si plusieurs ecritures se rapportent à cette facture
    plusieurs_ecritures = models.BooleanField(null=True, blank=True)
    # Si la facture est un échéancier
    periodicite = models.CharField(max_length=50,
                                   choices=[('aucune', 'aucune'), ('mensuel', 'mensuel'), ('trimestriel', 'trimestriel')],
                                   default='aucune')
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.date_emission) + ' - ' + self.emetteur



class Echeance(models.Model):
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    date_recouvrement = models.DateField()
    facture = models.ForeignKey(Facture, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date_recouvrement) + ' - ' + str(self.facture.emetteur) + ' - ' + str(self.facture.client)
