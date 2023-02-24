from django import forms
from comptabilite.facture.models import Facture, Echeance
from comptabilite.element_comptable.models import CategorieComptable, ElementComptable
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Field, Div, Row, Column
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
    emetteur = forms.CharField(max_length=50)
    client = forms.CharField(max_length=50,  required=False)
    date_emission = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    montant = forms.DecimalField()
    date_recouvrement = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),  required=False)
    plusieurs_ecritures = forms.BooleanField(initial=False, required=False)
    future_facture = forms.BooleanField(initial=False, required=False)
    ecriture_associee = forms.ModelMultipleChoiceField(
        queryset=ElementComptable.objects.filter(facture=None),  required=False)
    paiement_deja_constate = forms.BooleanField(initial=False, required=False)
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
        self.fact_id = kwargs.pop('facture') if 'facture' in kwargs.keys() else None
        self.echeances = kwargs.pop('echeances') if 'echeances' in kwargs.keys() else None
        self.montant = kwargs.pop('montant') if 'montant' in kwargs.keys() else None
        self.date_recouv = kwargs.pop('date_recouvrement') if 'date_recouvrement' in kwargs.keys() else None
        super(FactureForm, self).__init__(*args, **kwargs)
        if self.fact_id:
            facture = Facture.objects.get(id=self.fact_id)
            self.fields['type'].initial=facture.type
            self.fields['emetteur'].initial = facture.emetteur
            self.fields['client'].initial = facture.client
            self.fields['date_emission'].initial = facture.date_emission
            self.fields['plusieurs_ecritures'].initial = facture.plusieurs_ecritures
            self.fields['future_facture'].initial = facture.future_facture
            #self.fields['facture_liee'].initial = facture.facture_liee
            self.fields['periodicite'].initial = facture.periodicite
            self.fields['premiere_date'].initial = facture.date_debut
            self.fields['date_fin'].initial = facture.date_fin
            self.fields['montant'].initial = -self.montant if facture.type=='recue' else self.montant
            self.fields['date_recouvrement'].initial = self.date_recouv
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            Div(
                Row('type', css_class='m-2'),
                Row('emetteur', css_class='m-2'),
                Row('client', css_class='m-2'),
                Row('date_emission', css_class='m-2'),
                Row('montant', css_class='m-2'),
                Row('date_recouvrement', css_class='m-2'),
                Row('plusieurs_ecritures', css_class='m-2'),
                Row('future_facture', css_class='m-2'),
                Row(
                    Column('paiement_deja_constate', css_class='m-2'),
                    Column('ecriture_associee', css_class='m-2'),
                    css_class="card bg-light m-2 mb-3",
                ),
                Row(
                    Column('categorie_comptable', css_class='m-2'),
                    css_class='card bg-light m-2 mb-5',
                )
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

