from datetime import datetime as dt
import django.db.models.fields as djangofield
from django.apps import apps

def check_colonnes(cols, match, col_initiale):
    # Verifie que la les colonnes definies dans la base ont toutes un equivalent dans le csv
    # Retourne True et une liste vide si toutes les colonnes sont présentes
    # Sinon retourne False et la liste des colonnes manquantes

    flag = True
    liste = []

    for m in match:
        if m[col_initiale] not in cols:
            liste.append(m[col_initiale])
            flag = False

    return flag, liste


def check_doublons(DBClass, liste, match, champ_cible, flag_doublon):
    # Retourne la liste de doublons à partir des criteres colonnes (flag doublon True)

    def champ_doublon(nom_ch_cible, nom_fl_doublon, champ_cible, match):
        # Retourne True si le champ doit être vérifié pour les doublons
        return {v[nom_ch_cible]: v[nom_fl_doublon] for v in match}[champ_cible]

    # liste des champs qui caractérisent les doublons
    l0 = [{k: v for k, v in l.items() if champ_doublon(champ_cible, flag_doublon, k, match)} for l in liste]
    doublons = []
    reste = []

    for l1, l2 in zip(liste, l0):
        if DBClass.objects.filter(**l2):
            doublons.append(l1)
        else:
            reste.append(l1)

    return doublons, reste


def dict_bon_format(DBClass, dico, dec_sep, date_form):
    # Met les champs date et nombre au bon format
    # dec_sep: séparateur de céimales
    # date_form: format de date python, par ex %d/%m/%YY

    for k, v in dico.items():

        if type(DBClass._meta.get_field(k)) == djangofield.DecimalField:
            s = v.replace(dec_sep, '.')
            dico[k] = float(s) if s != '' else 0

        if type(DBClass._meta.get_field(k)) == djangofield.DateField:
            dico[k] = dt.strptime(v, date_form)

    return dico


def creer_dict(ViewClass, dico, match):
    d = dict()
    for v in match:
        if v[ViewClass.champ_flag_fk] == False:
            d[v[ViewClass.champ_cible]] = dico[v[ViewClass.col_initiale]]
        else:
            Mod = apps.get_model(app_label=ViewClass.app_name, model_name=v[ViewClass.champ_classe_liee])
            val = dico[v[ViewClass.col_initiale]]
            d[v[ViewClass.champ_cible]] = Mod.objects.get(**{v[ViewClass.champ_cible]: val})
    return d