from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from datetime import datetime as dt

from comptabilite.element_comptable.models import ElementComptable

# Create your views here.

class ResultatEntreDates(View):

    template_name = 'resultat.html'

    def get_context_data(self, *args, **kwargs):

        def agg(obj, cat):
            ret = {}
            for c in cat:
                m = obj.filter(categorie=c).aggregate(Sum('montant'))['montant__sum']
                m = 0 if m==None else float(m)
                ret[c[0]] = m
            return ret

        date_debut = dt.strptime(self.request.GET.get('debut'), '%Y-%m-%d')
        date_fin = dt.strptime(self.request.GET.get('fin'), '%Y-%m-%d')
        elem = ElementComptable.objects.filter(date__gte=date_debut, date__lte=date_fin)
        cat = elem.values_list('categorie')
        cat1 = elem.values_list('categorie__intitule')
        credit = agg(elem.filter(montant__gte=0), cat)
        debit = agg(elem.filter(montant__lte=0), cat)


        resultat = elem.aggregate(Sum('montant'))['montant__sum']
        return { 'date_debut': self.request.GET.get('debut'),
                 'date_fin' : self.request.GET.get('fin'),
                 'categories': {c1[0]:[credit[c[0]], debit[c[0]]] for c, c1 in zip(cat, cat1)},
                 'resultat' : resultat,
                 }

    def get(self, request):
        return render(self.request, self.template_name, self.get_context_data())
