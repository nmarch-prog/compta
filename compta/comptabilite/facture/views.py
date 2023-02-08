from django.shortcuts import render
from django.views.generic import CreateView, FormView
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from comptabilite.element_comptable.models import ElementComptable
from .models import Facture, Echeance
from .forms import FactureCategorieForm, FactureSimple, EcheanceFactureSimple, FactureForm
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from simple_rest import Resource
from django.core import serializers
from django.core.files.storage import FileSystemStorage
import json
import pandas as pd
from .utils import creer_fact_echeances
import csv
from django.forms.models import model_to_dict
import decimal

# Create your views here.

class FactureCategorie(FormView):

    form_class = FactureCategorieForm
    template_name = 'nouvelle_facture_categorie.html'

    def form_valid(self, form):
        cat = form.cleaned_data.pop('categorie')
        montant = form.cleaned_data['montant']
        date = form.cleaned_data['date_emission']
        if form.is_valid():
            truc = form.save()
        ElementComptable.objects.create(facture=truc,
                                        montant=montant,
                                        date=date,
                                        categorie=cat)
        return render(self.request, 'nouvelle_facture_categorie.html')



class NouvelleFactureEmise(CreateView):

    model = Facture
    fields = '__all__'


class NouvelleFactureSimple(FormView):

    template_name = 'facture/nouvelle_facture_simple.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        print(context)
        return context



    def get(self, request, *args, **kwargs):
        #print(self.get_context_data(**kwargs))
        #context = super().get_context_data(**kwargs)
        context = {}
        facture_simple_form = FactureSimple()
        facture_simple_form.prefix = 'facture_simple_form'
        echeance_simple_form = EcheanceFactureSimple()
        echeance_simple_form.prefix = 'echeance_simple_form'
        context['facture_simple_form'] = facture_simple_form
        context['echeance_simple_form'] = echeance_simple_form
        #return self.render_to_response(self.get_context_data())
        return self.render_to_response(context)


class TestForm(FormView):

    template_name='facture/testform.html'
    form_class = FactureForm


    def post(self, request, *args, **kwargs):
        form = request.POST
        creer_fact_echeances(form)

        # Crée l'objet facture
        # fact = Facture.objects.create(
        #     type=form['type'],
        #     emetteur=form['emetteur_ou_client'],
        #     date_emission=form['date_emission'],
        #     fichier=form['fichier'] if form['fichier']!='' else None,
        #     future_facture=True if hasattr(form, 'future_facture') else False,
        # )
        #
        # # Cree les echeances liées à la facture
        # if form['periodicite']=='aucune':
        #     Echeance.objects.create(
        #         montant=float(form['montant']) if form['type']=='emise' else -float(form['montant']),
        #         date_recouvrement=form['date_recouvrement'],
        #         facture=fact
        #     )
        # else:
        #     dates = [form['premiere_date'], form['date_fin']]
        #     start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        #     delta = relativedelta(end, start)
        #     months = delta.months + delta.years * 12
        #     mt = float(form['montant'] if form['type'] == 'emise' else -float(form['montant']))
        #     n = 1 if form['periodicite']==1 else 3
        #     for d in [start+relativedelta(months=x*n) for x in range(0,int(months/n)+1)]:
        #         Echeance.objects.create(
        #             montant=mt/(int(months/n)+1),
        #             date_recouvrement=d,
        #             facture=fact
        #         )
        #
        # # Si apporteur ou commercial, cree la facture secondaire et les echeances liées
        # if form['commercial']!='':
        #     fact_com = Facture.objects.create(
        #         type='recue',
        #         emetteur=form['commercial'],
        #         date_emission=form['date_retro_commercial'],
        #         future_facture=True,
        #     )
        #     Echeance.objects.create(
        #         montant=-form['retrocession_commercial'],
        #         date_recouvrement=form['date_retro_commercial'],
        #         facture=fact_com
        #     )
        # if form['apporteur']!='':
        #     fact_app = Facture.objects.create(
        #         type='recue',
        #         emetteur=form['apporteur'],
        #         date_emission=form['date_retro_apporteur'],
        #         future_facture=True,
        #     )
        #     Echeance.objects.create(
        #         montant=-form['retrocession_apporteur'],
        #         date_recouvrement=form['date_retro_apporteur'],
        #         facture=fact_app
        #     )

        # Cree l'element comptable lié (pas si echeancier car service non fourni)


        return HttpResponseRedirect('/')


def echeances_vue(request):
    return render(request, 'facture/testliste.html')

class EcheancesView(Resource):

    def get(self, request):
        echeances = Echeance.objects.all() \
            .filter(date_recouvrement__gte = request.GET.get('date')).order_by('date_recouvrement')
        print(serializers.serialize('json', echeances))
        truc = echeances.values()
        somme = 0
        d = dict()
        for t in truc:
            somme += t['montant']
            t['cumul'] = somme

        #print(self.to_json(truc))
        return JsonResponse(self.to_json_adapted(echeances),safe=False)
        #return HttpResponse(self.to_json(echeances), content_type='application/json', status=200)
        #return JsonResponse(json.loads(truc), safe=False)

    # def to_json(self, objects):
    #     raw = serializers.serialize('python', objects)
    #     act_data = [d['fields'] for d in raw]
    #     act_data = [dict((k, float(a)) if isinstance(a, decimal.Decimal) else (k,a) for k, a in b.items()) for b in act_data]
    #     act_data = [dict((k, datetime.strftime(a, '%Y-%m-%d')) if isinstance(a, date) else (k, a) for k, a in b.items()) for b in
    #                 act_data]
    #     print(act_data)
    #     return json.dumps(act_data)

    def to_json_adapted(self, objects):
        json_data = serializers.serialize('json', objects)
        json_final = {"total": objects.count(), "rows": []}
        data = json.loads(json_data)
        somme = 0
        for item in data:
            del item["model"]
            item["fields"].update({"id": item["pk"]})
            item = item["fields"]
            somme += float(item["montant"])
            item["cumul"] = "{:.2f}".format(somme)
            item["facture2"] = Facture.objects.get(id=item["facture"]).emetteur
            json_final['rows'].append(item)
        return json_final


    def to_json(self, objects):
        json_data = serializers.serialize('json', objects)
        json_final = {"total": objects.count(), "rows": []}
        data = json.loads(json_data)
        for item in data:
            del item["model"]
            item["fields"].update({"id": item["pk"]})
            item = item["fields"]
            json_final['rows'].append(item)
        return json_final

    # def to_json(self, objects):
    #     return serializers.serialize('json', objects)


def import_csv_factures(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        excel_file = uploaded_file_url
        with open("." + excel_file, encoding='unicode_escape') as f:
            a = [{k: v for k, v in row.items()}
                 for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]
        empexceldata = pd.read_csv("." + excel_file, encoding='unicode_escape', sep=';')
        dbframe = empexceldata.to_dict(orient='records')
        for dbf in a:
            creer_fact_echeances(dbf)

        return HttpResponseRedirect('factures/liste/')
    return render(request, 'facture/importexcel.html', {})