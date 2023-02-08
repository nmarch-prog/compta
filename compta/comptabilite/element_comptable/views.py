from django.shortcuts import render
from django.views.generic import FormView
from django.forms import formset_factory
from .forms import EcrituresNonComptabiliseesForm, EcrituresNonComptabiliseesFacturesForm
from comptabilite.ecriture.models import Ecriture
from comptabilite.facture.models import Facture
from comptabilite.element_comptable.models import ElementComptable

# Create your views here.

class EcrituresNonComptabiliseesView(FormView):
    # 2e etape de l'insertion des ecritures, si pas de facture présente on categorise

    template_name = 'element_comptable/categorisation_ecritures.html'
    form_class = EcrituresNonComptabiliseesForm

    def get_form_kwargs(self):
        kw = super(EcrituresNonComptabiliseesView, self).get_form_kwargs()
        kw['liste'] = [(str(e.id), e.__str__()) for e  in Ecriture.objects.exclude(id__in=ElementComptable.objects.all().\
                                                values_list('ecriture')).exclude(hors_compta=True)]
        return kw

    def form_valid(self, form):
        for a in zip(list(form.cleaned_data.keys())[0::2], list(form.cleaned_data.values())[1::2]):
            ecr = Ecriture.objects.get(id=a[0])
            ElementComptable.objects.create(ecriture=ecr,
                                            categorie=a[1],
                                            montant=ecr.credit if ecr.debit==0 else -ecr.debit,
                                            date=ecr.date_operation,)
        return render(self.request, 'element_comptable/categorisation_ecritures.html')


#class ComptabiliteMensuelle

class EcrituresNonComptabiliseesFacturesView(FormView):
    # 1e étape de l'importation des ecritures, on associe à des factures (element comptable existant)

    template_name = 'association_ecritures.html'
    form_class = EcrituresNonComptabiliseesFacturesForm

    def get_form_kwargs(self):
        kw = super(EcrituresNonComptabiliseesFacturesView, self).get_form_kwargs()
        kw['liste'] = [(str(e.id), e.__str__()) for e in Ecriture.objects.exclude(id__in=ElementComptable.objects.all(). \
                                                                                  values_list('ecriture')).exclude(
            hors_compta=True)]
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



