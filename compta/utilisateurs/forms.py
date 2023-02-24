from django import forms
from .models import Collaborateur, Courtier


class CollaborateurModelForm(forms.ModelForm):

    class Meta:
        model = Collaborateur
        fields = ['user', 'droit_gestion_utilisateurs', 'droit_comptabilite', 'droit_suivi_clients', 'statut']


class CourtierModelForm(forms.ModelForm):

    class Meta:
        model = Courtier
        fields = ['collaborateur', 'zone']
