from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.forms import formset_factory
from django.db.models import Q, Sum, Value
from .forms import BaseEcrituresForm
from comptabilite.ecriture.models import Ecriture
from comptabilite.facture.models import Facture
from comptabilite.element_comptable.models import ElementComptable, CategorieComptable

# Create your views here.

def calc_montant(e):
    if e.debit==None or e.debit==0: return float(e.credit)
    return -float(e.debit)

def get_cat_comptable(req, i):
    id = req.POST['form-' + str(i) + '-categorie_comptable']
    return CategorieComptable.objects.get(id=id)

def get_facture(req, i):
    id = req.POST['form-' + str(i) + '-facture']
    return Facture.objects.get(id=id)


class EcrituresNonComptabiliseesView(FormView):
    # 2e etape de l'insertion des ecritures, si pas de facture présente on categorise

    template_name = 'element_comptable/categorisation_ecritures.html'
    #form_class = EcrituresNonComptabiliseesForm2
    form_class = BaseEcrituresForm
    form = formset_factory(BaseEcrituresForm)

    def get(self, request):
        ecr = [e for e  in Ecriture.objects.exclude(
            id__in=[e[0] for e in ElementComptable.objects.all().values_list('ecriture')]).
                    exclude(hors_compta=True)]
        fs = formset_factory(BaseEcrituresForm, extra=len(ecr))
        context = {
            'formset': fs,
            'ecritures': ecr,
            'zip': zip(list(fs()), ecr),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        ecr = [e for e in Ecriture.objects.exclude(
            id__in=[e[0] for e in ElementComptable.objects.all().values_list('ecriture')]).
                    exclude(hors_compta=True)]
        elem_compta_multiples=[]
        for i, e in zip(range(0, int(request.POST['form-TOTAL_FORMS'])), ecr):
            if request.POST.get('form-' + str(i) + '-hors_compta')!=None:
                e.hors_compta = True
                e.save()
                continue
            if request.POST['form-' + str(i) + '-categorie_comptable']!='':
                # Creer un élément comptable de la bonne catégorie
                ElementComptable.objects.create(ecriture=e,
                                                categorie=get_cat_comptable(request, i),
                                                montant=calc_montant(e),
                                                date=e.date_operation,)
                continue
            if request.POST['form-' + str(i) + '-facture']!='':
                # Lier l'écriture à l'élément comptable existant lié à la facture
                # Problème si facture avec plusieurs elements comptables
                e2 = ElementComptable.objects.filter(facture=get_facture(request, i))
                if e2.count()>1:
                    elem_compta_multiples.append(e, e2)
                else:
                    e2 = e2.get()
                    e2.ecriture = e
                    e2.save()
                continue

        return render(request, 'element_comptable/categorisation_ecritures.html')



class EcrituresNonComptabiliseesFacturesView(FormView):
    # 1e étape de l'importation des ecritures, on associe à des factures (element comptable existant)

    template_name = 'association_ecritures.html'
    #form_class = EcrituresNonComptabiliseesFacturesForm

    def get_form_kwargs(self):
        kw = super(EcrituresNonComptabiliseesFacturesView, self).get_form_kwargs()
        kw['liste'] = [(str(e.id), e.__str__(),e) for e in \
                       Ecriture.objects.exclude(id__in=ElementComptable.objects.all().
                           values_list('ecriture')).exclude(hors_compta=True)]
        kw['factures'] = Facture.objects.exclude(id__in=ElementComptable.objects.all().values_list('facture'))
        return kw

    def form_valid(self, form):
        for a in zip(list(form.cleaned_data.keys())[0::2], list(form.cleaned_data.values())[1::2]):
            ecr = Ecriture.objects.get(id=a[0])
            # update de l'element comptable associe a la facture avec l'ecriture
            # ulterieurement, mettre des regles si changement de categorie comptable une fois que la
            # facture est reglee, et verifier que les montants correspondent
            elem_comptable = ElementComptable.objects.get(facture=a[1])
            elem_comptable.ecriture = Ecriture.objects.get(id=a[0])
            elem_comptable.save()
        return render(self.request, 'element_comptable/categorisation_ecritures.html')


class ComptaMensuelleView(ListView):

    template_name = 'element_comptable/vue_comptable.html'

    def get_queryset(self):
        mois = int(self.kwargs['mois'].split('-')[1])
        annee = int(self.kwargs['mois'].split('-')[0])
        ec = ElementComptable.objects.filter(
            Q(date__month=mois) & Q(date__year=annee))
        total = ec.aggregate(sum=Sum('montant'))['sum']
        credit = ec.filter(montant__gte=0).aggregate(sum=Sum('montant'))['sum']
        debit = ec.filter(montant__lte=0).aggregate(sum=Sum('montant'))['sum']
        qs = CategorieComptable.objects.filter(Q(categorieelem__date__month=mois) & Q(categorieelem__date__year=annee)).annotate(
            total=Sum('categorieelem__montant')).annotate(
            resultat=Value(total) if total!=None else Value(0),
            credit=Value(credit) if credit!=None else Value(0),
            debit=Value(debit)) if debit!=None else Value(0)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total']=self.object_list.aggregate(sum=Sum('total'))['sum']
        context['credit']=self.object_list.filter(total__gte=0).aggregate(sum=Sum('total'))['sum']
        context['debit']=self.object_list.filter(total__lte=0).aggregate(sum=Sum('total'))['sum']
        return context

