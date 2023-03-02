from .models import ElementComptable, CategorieComptable
from comptabilite.ecriture.models import Ecriture
from comptabilite.facture.models import Facture
from django import forms
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Field, Div, Row, Column


class BaseEcrituresForm(forms.Form):

    hors_compta = forms.BooleanField()
    categorie_comptable = forms.ModelChoiceField(queryset=CategorieComptable.objects.all())
    facture = forms.ModelChoiceField(queryset=Facture.objects.filter(
        Q(id__in=ElementComptable.objects.filter(ecriture=None).values_list('facture'))\
        | Q(plusieurs_ecritures=True))
    )









