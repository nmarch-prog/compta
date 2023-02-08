from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import FormView, RedirectView
import django.db.models.fields as djangofield
from comptabilite.ecriture.models import Ecriture, Compte
from comptabilite.element_comptable.models import ElementComptable, CategorieComptable

from afpi_import_csv.views import ImportCsvView
from afpi_import_csv.forms import ImportCsvForm
from afpi_import_csv.tools import dict_bon_format
from afpi_import_csv.models import FormatCsv, CorrespondanceColonnes


class ImportEcrituresCsv(ImportCsvView):

    template_name = 'import_ecritures.html'
    template_render_name = 'post_import.html'
    form_class = ImportCsvForm
    model_class = Ecriture

    intitule_type_fichier = 'compte'
    inclure_type_fichier_base = True
    type_fichier_base_fk = True
    type_fichier_model_class = Compte
    type_fichier_nom_champ = 'nom'


class ImportEcrituresCategoriesCsv(ImportEcrituresCsv):

    def form_valid(self, form):

        lines, cols, match, type_fichier, csv_data = self.lecture_fichier(form)
        flag, cols_manquantes, doublons = self.enregistrement_donnees(lines, cols, match, type_fichier, csv_data)

        if not flag:
            return render(self.request, self.template_render_name, self.get_context_data(manquantes=cols_manquantes))

        dico_cols = {c['colonne_initiale']:c['champ_cible'] for c in match}
        liste_cols = [c['colonne_initiale'] for c in match]
        #cols_cible = [CorrespondanceColonnes.objects.filter(type_fich__nom=type_fichier, col_initiale=c).\
        #    values(self.champ_cible) for c in cols]

        for l in lines[1:]:
            dico1 = dict(zip(cols, l.split(csv_data['csv_field'])))
            dico2 = dict_bon_format(Ecriture, {dico_cols[x]: dico1[x] for x in liste_cols},
                                    csv_data['dec_sep'], csv_data['date_form'])
            print(dico2)
            e = Ecriture.objects.get(**dico2)
            ElementComptable.objects.create(ecriture=e,
                                            categorie=CategorieComptable.objects.get(no_compta=dico1['Categorie']),
                                            montant=e.credit if e.debit==0 else -e.debit,
                                            date=e.date_operation)

        return render(self.request, self.template_render_name, self.get_context_data(doublons=doublons))

