from django.db import models

from .ecriture.models import Ecriture
from .facture.models import Facture
from .element_comptable.models import ElementComptable, CategorieComptable

# Create your models here.

# class ElementComptable(models.Model):
#
#     facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
#     ecriture = models.ForeignKey(Ecriture, on_delete=models.CASCADE)
#     categorie = models.CharField(max_length=20)
#     besoin_facture = models.BooleanField(default=True)