from django import forms

from .models import TypeFichier

class ImportCsvForm(forms.Form):
    fichier = forms.FileField()
    type_fichier = forms.ChoiceField(choices=zip([i[0] for i in TypeFichier.objects.all().values_list('nom')],
                                           [i[0] for i in TypeFichier.objects.all().values_list('nom')]))




