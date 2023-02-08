from .models import ElementComptable, CategorieComptable
from comptabilite.ecriture.models import Ecriture
from django import forms

class EcrituresNonComptabiliseesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        liste = kwargs.pop('liste')
        super(EcrituresNonComptabiliseesForm, self).__init__(*args, **kwargs)
        for e in liste:
            self.fields[e[0]] = forms.IntegerField(required=False, widget=forms.HiddenInput())
            self.fields[e[1]] = forms.ModelChoiceField(queryset=CategorieComptable.objects.all())


class EcrituresNonComptabiliseesFacturesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        liste = kwargs.pop('liste')
        factures = kwargs.pop('factures')
        super(EcrituresNonComptabiliseesFacturesForm, self).__init__(*args, **kwargs)
        for e in liste:
            self.fields[e[0]] = forms.IntegerField(required=False, widget=forms.HiddenInput())
            self.fields[e[1]] = forms.ModelChoiceField(queryset=factures)







