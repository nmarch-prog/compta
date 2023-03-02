from django.db import models
from comptabilite.ecriture.models import Ecriture
from comptabilite.facture.models import Facture

# Create your models here.

class CategorieComptable(models.Model):

    intitule = models.CharField(max_length=40)
    no_compta = models.IntegerField()

    def __str__(self):
        return self.intitule

class ElementComptable(models.Model):

    ecriture = models.ForeignKey(Ecriture, null=True, blank=True, on_delete=models.CASCADE)
    facture = models.ForeignKey(Facture, null=True, blank=True, on_delete=models.CASCADE)
    categorie = models.ForeignKey(CategorieComptable, on_delete=models.CASCADE, related_name='categorieelem')
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(blank=True, null=True)

    # class Meta:
    #     # Verification qu'au moins une ecriture ou une facture est liée
    #     constraints = [
    #         models.CheckConstraint(
    #             name="%(app_label)s_%(class)s_facture_or_ecriture",
    #             check=(
    #                     models.Q(ecriture__isnull=True, facture__isnull=False)
    #                     | models.Q(ecriture__isnull=False, facture__isnull=True)
    #             ),
    #         )
    #     ]

    def __str__(self):
        return str(self.date) + ' - ' + self.categorie.intitule + ' - ' + str(self.montant)
