from django import forms

from .models import Ecriture, Compte

class ImportEcritureCsvForm(forms.Form):
    fichier = forms.FileField()
    compte = forms.ChoiceField(choices=zip([i[0] for i in Compte.objects.all().values_list('id')],
                                           [i[0] for i in Compte.objects.all().values_list('nom')]))




