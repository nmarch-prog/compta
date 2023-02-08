
from django.shortcuts import render
from django.views.generic import FormView
from .forms import ImportCsvForm
from afpi_import_csv.models import CorrespondanceColonnes, TypeFichier, FormatCsv
#from comptabilite.models import Ecriture

from afpi_import_csv.tools import check_colonnes, check_doublons, dict_bon_format, creer_dict

IMPORT_ECRITURE_CSV_TEMPLATE = 'import_ecritures.html'

# Import de fichiers CSV
# Utilise une table de la database nommee FormatCsv qui contient la description du format
# en fonction du compte bancaire choisi


class ImportCsvView(FormView):
    # Importe un fichier csv releve de compte bancaire
    # La correspondance entre les champs de la classe Ecriture et du fichier
    # se fait par la classe CorrepondanceColonnes
    # Les doublons sont identifies par des valeurs identiques dans les colonnes
    # dont le flag doublon est True

    # Infos externes au modèle ImportCsv, à renseigner dans une classe qui en dérive
    template_name = IMPORT_ECRITURE_CSV_TEMPLATE
    template_render_name = 'post_import.html'
    form_class = ImportCsvForm
    #model_class = Ecriture
    #intitule_type_fichier = 'compte'
    #model_class = TestModel2

    # Info internes au modèle ImportCsv
    col_initiale = 'colonne_initiale'
    champ_cible = 'champ_cible'
    champ_flag_doublon = 'flag_doublon'
    champ_flag_fk = 'flag_foreignkey'
    champ_classe_liee = 'classe_liee'
    champ_ident_classe = ''
    form_champ_fichier = 'fichier'
    form_champ_type_fichier = 'type_fichier'
    app_name = __package__


    def lecture_fichier(self, form):

        # Recupération des données du formulaire
        csv_file = form.cleaned_data[self.form_champ_fichier]
        type_fichier = form.cleaned_data[self.form_champ_type_fichier]

        # Récupération des données de format CSV
        csv_data = {
            'csv_enc' : FormatCsv.objects.get(type_fich__nom=type_fichier).csv_encoding,
            'csv_line' : FormatCsv.objects.get(type_fich__nom=type_fichier).csv_line_separator,
            'csv_field' : FormatCsv.objects.get(type_fich__nom=type_fichier).csv_field_separator,
            'dec_sep' : FormatCsv.objects.get(type_fich__nom=type_fichier).decimal_separator,
            'date_form' : FormatCsv.objects.get(type_fich__nom=type_fichier).date_format
        }


        # Ouverture du fichier
        lines = csv_file.read().decode(csv_data['csv_enc']).splitlines()  # split(csv_line)
        cols = lines[0].split(csv_data['csv_field'])

        # Liste des champs et de leur correspondance
        match = list(CorrespondanceColonnes.objects.filter(type_fich__nom=type_fichier).values(self.col_initiale,
                                                                                               self.champ_cible,
                                                                                               self.champ_flag_doublon,
                                                                                               self.champ_flag_fk,
                                                                                               self.champ_classe_liee))

        return lines, cols, match, type_fichier, csv_data


    def enregistrement_donnees(self, lines, cols, match, type_fichier, csv_data):

        # Determinations des champs manquants
        flag, cols_manquantes = check_colonnes(cols, match, self.col_initiale)

        if flag:  # Si tous les champs sont presents dans le fichier CSV

            # Determination des doublons
            liste = []
            for l in lines[1:]:
                d1 = creer_dict(self, dict(zip(cols, l.split(csv_data['csv_field']))), match)
                liste.append(dict_bon_format(self.model_class, d1, csv_data['dec_sep'], csv_data['date_form']))
            doublons, reste = check_doublons(self.model_class, liste, match, self.champ_cible,
                                                       self.champ_flag_doublon)

            # Import en base
            for r in reste:
                if hasattr(self, 'intitule_type_fichier'):
                    if self.type_fichier_base_fk:
                        r[self.intitule_type_fichier] = self.type_fichier_model_class.objects.get(
                            **{self.type_fichier_nom_champ: type_fichier}
                        )
                    else:
                        r[self.intitule_type_fichier] = type_fichier
                self.model_class.objects.create(**r)

        return flag, cols_manquantes, doublons


    def form_valid(self, form):

        lines, cols, match, type_fichier, csv_data = self.lecture_fichier(form)
        flag, cols_manquantes, doublons = self.enregistrement_donnees(lines, cols, match, type_fichier, csv_data)

        if flag: # Si tous les champs sont presents dans le fichier CSV

            return render(self.request, self.template_render_name, self.get_context_data(doublons=doublons))

        else: # Si il manque des champs dans le fichier CSV
            return render(self.request, self.template_render_name, self.get_context_data(manquantes=cols_manquantes))
