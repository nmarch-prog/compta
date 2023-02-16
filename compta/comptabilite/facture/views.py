from django.shortcuts import render
from django.views.generic import CreateView, FormView, ListView
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Sum
from django.http.response import HttpResponse
from comptabilite.element_comptable.models import ElementComptable, CategorieComptable
from .models import Facture, Echeance
from .forms import FactureCategorieForm, FactureSimple, EcheanceFactureSimple, FactureForm
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from simple_rest import Resource
from django.core import serializers
from django.core.files.storage import FileSystemStorage
import json
import pandas as pd
from .utils import creer_maj_facture, creer_echeances, creer_facture_echeance_liees
import csv
from django.forms.models import model_to_dict
import decimal

# Create your views here.


def traitement_form_facture(form, facture):

    # Creer ou maj facture
    fact = creer_maj_facture(form, facture)

    if form['commercial'] != '': creer_facture_echeance_liees(form, fact, 'commercial')
    if form['commercial_2'] != '': creer_facture_echeance_liees(form, fact, 'commercial_2')
    if form['apporteur'] != '': creer_facture_echeance_liees(form, fact, 'apporteur')

    if 'paiement_deja_constate' in form:
        # Associer element comptable
        return HttpResponseRedirect('factures/associer_element_comptable/' + str(fact.id))
    else:
        creer_echeances(form, fact)
        # Creer element comptable si facture non future
        print(form)
        if not ('future_facture' in form) or form['future_facture']=='':
            ElementComptable.objects.create(
                facture=fact,
                categorie=CategorieComptable.objects.get(id=form['categorie_comptable']),
                montant=float(form['montant'].replace(',', '.')) if form['type'] == 'emise' \
                    else -float(form['montant'].replace(',', '.')),
                date=form['date_emission'],
            )

    return HttpResponseRedirect('/factures/liste')


class TestForm(FormView):

    template_name='facture/testform.html'
    form_class = FactureForm

    def get_form_kwargs(self):
        # Passe les données de la facture si édition
        facture = self.kwargs['facture'] if 'facture' in self.kwargs.keys() else None
        kwargs = super(TestForm, self).get_form_kwargs()
        if facture==None: return kwargs
        ech = Echeance.objects.filter(facture=facture)
        m = ech.aggregate(Sum('montant'))['montant__sum']
        kwargs['echeances'] = ech.values_list('id')
        kwargs['montant'] = m if m!=None else 0
        kwargs['date_recouvrement'] = ech.values('date_recouvrement')[0]['date_recouvrement'] \
            if Facture.objects.get(id=facture).periodicite=='aucune' else None
        kwargs['facture'] = facture
        return kwargs

    def post(self, request, *args, **kwargs):
        form = request.POST
        facture = self.kwargs['facture'] if 'facture' in self.kwargs.keys() else None
        return traitement_form_facture(form, facture)




def echeances_vue(request):
    return render(request, 'facture/testliste.html')

class EcheancesView(Resource):

    def regroupement(self, echeances, contreparties, dates):
        l = []
        for c in contreparties:
            for d in dates:
                m = echeances.filter(facture__emetteur=c, date_recouvrement=d).aggregate(Sum('montant'))['montant__sum']
                l.append({'montant': m, 'date_recouvrement': d, 'intitule': c})
        for e in echeances.exclude(facture__emetteur__in=contreparties, date_recouvrement__in=dates).\
                values('montant', 'date_recouvrement', 'facture__emetteur', 'facture__client'):
            l.append({'montant':e['montant'],
                      'date_recouvrement': datetime.strftime(e['date_recouvrement'], '%Y-%m-%d'),
                      'intitule': e['facture__emetteur'] + ' ' + e['facture__client']
                      })
        l2 = sorted(l, key=lambda d: d['date_recouvrement'])
        somme=0
        for l in l2:
            somme += l['montant']
            l['total'] = "{:.2f}".format(somme)
            l['montant'] = "{:.2f}".format(l['montant'])
        return {'total': len(l2), 'rows': l2}

    def get(self, request):
        echeances = Echeance.objects.all() \
            .filter(date_recouvrement__gte = request.GET.get('date')).order_by('date_recouvrement')
        res = self.regroupement(echeances, ['ACTI', 'Elan'], ['2023-02-20'])
        return JsonResponse(res, safe=False)



def import_csv_factures(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        excel_file = uploaded_file_url
        with open("." + excel_file, encoding='utf8') as f:
            a = [{k: v for k, v in row.items()}
                 for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]
        for dbf in a:
            fact=traitement_form_facture(dbf, None)
        return HttpResponseRedirect('factures/liste/')
    return render(request, 'facture/importexcel.html', {})

class VueMensuelleMandataire(ListView):

    template_name = 'facture/mandataire.html'

    def get_queryset(self):
        mois = int(self.kwargs['mois'].split('-')[1])
        annee = int(self.kwargs['mois'].split('-')[0])
        return Echeance.objects.filter(
            facture__emetteur=self.kwargs['mandataire'],
            date_recouvrement__month=mois,
            date_recouvrement__year=annee)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = kwargs.pop('object_list', self.object_list)
        context['total'] = "{:.2f}".format(qs.aggregate(Sum('montant'))['montant__sum']) if qs else 0
        return context

class VueEcrituresSansFacture(ListView):

    template_name = ''

    def get_queryset(self):
        return ElementComptable.objects.filter(facture=None)


class VueAssocierElemComptFacture(FormView):

# Mettre directement dans le formulaire une dropdown avec la liste des ecritures sans facture
    template_name = 'facture/testform.html'
    form_class = FactureForm