from django.contrib import admin
from .ecriture.models import Compte, Ecriture
from .facture.models import Facture, Echeance
from .element_comptable.models import ElementComptable, CategorieComptable

# Register your models here.

admin.site.register(Compte)
admin.site.register(Ecriture)
admin.site.register(Facture)
admin.site.register(ElementComptable)
admin.site.register(CategorieComptable)
admin.site.register(Echeance)