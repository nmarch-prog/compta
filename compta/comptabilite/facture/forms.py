from django import forms
from comptabilite.facture.models import Facture, Echeance
from comptabilite.element_comptable.models import CategorieComptable
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Field, Div, Row
from crispy_forms.bootstrap import TabHolder, Tab

class FactureCategorieForm(forms.ModelForm):

    categorie = forms.ModelChoiceField(queryset=CategorieComptable.objects.all())

    class Meta:
        model = Facture
        fields = '__all__'


class FactureSimple(forms.ModelForm):

    class Meta:
        model = Facture
        fields = '__all__'

    helper = FormHelper()
    helper.form_tag = True


class EcheanceFactureSimple(forms.ModelForm):

    class Meta:
        model = Echeance
        fields = '__all__'

    helper = FormHelper()
    helper.form_tag = True



class FactureForm(forms.Form):

    type = forms.ChoiceField(choices=[('emise', 'emise'), ('recue', 'recue')])
    emetteur_ou_client = forms.CharField(max_length=50)
    date_emission = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    montant = forms.DecimalField()
    date_recouvrement = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    future_facture = forms.BooleanField(initial=False, required=False)
    categorie_comptable = forms.ModelChoiceField(queryset=CategorieComptable.objects.all(),  required=False)

    fichier = forms.FileField(required=False)

    commercial = forms.CharField(max_length=20, required=False)
    retrocession_commercial = forms.DecimalField(required=False)
    date_retro_commercial = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)

    commercial_2 = forms.CharField(max_length=20, required=False)
    retrocession_commercial_2 = forms.DecimalField(required=False)
    date_retro_commercial_2 = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)

    apporteur = forms.CharField(max_length=20, required=False)
    retrocession_apporteur = forms.DecimalField(required=False)
    date_retro_apporteur = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)

    periodicite = forms.ChoiceField(choices=[('aucune', 'aucune'),('mensuel', 'mensuel'),
                                             ('trimestriel', 'trimestriel')], required=False)
    premiere_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    date_fin = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Div(
                Row('type', css_class='m-2'),
                Row('emetteur_ou_client', css_class='m-2'),
                Row('date_emission', css_class='m-2'),
                Row('montant', css_class='m-2'),
                Row('date_recouvrement', css_class='m-2'),
                Row('future_facture', css_class='m-2'),
                Row('categorie_comptable', css_class='m-2')
            ),
            Div(
                TabHolder(
                    Tab(
                        'Fichier',
                        Row('fichier', css_class='m-5')
                    ),
                    Tab(
                        'Apporteur',
                        Row('apporteur', css_class='m-2'),
                        Row('retrocession_apporteur', css_class='m-2'),
                        Row('date_retro_apporteur', css_class='m-2'),
                    ),
                    Tab(
                        'Commercial',
                        Row('commercial', css_class='m-2'),
                        Row('retrocession_commercial', css_class='m-2'),
                        Row('date_retro_commercial', css_class='m-2'),
                    ),
                    Tab(
                        'Commercial 2',
                        Row('commercial_2', css_class='m-2'),
                        Row('retrocession_commercial_2', css_class='m-2'),
                        Row('date_retro_commercial_2', css_class='m-2'),
                    ),
                    Tab(
                        'Echeancier',
                        Row('periodicite', css_class='m-2'),
                        Row('premiere_date', css_class='m-2'),
                        Row('date_fin', css_class='m-2'),
                    ),
                ),
            ),
            Div(

            ),
            Div(
                Submit('submit', 'Sauver', css_class="btn btn-primary"),

            )
        )








