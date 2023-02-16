from .models import Facture, Echeance
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

def creer_maj_facture(formdata, facture):

    params = {
        'type': formdata['type'],
        'emetteur': formdata['emetteur'],
        'client': formdata['client'],
        'date_emission': formdata['date_emission'] if formdata['date_emission'] != '' else None,
        'fichier': None if (not (hasattr(formdata, 'fichier')) or (formdata['fichier'] != '')) else formdata['fichier'],
        'future_facture': True if hasattr(formdata, 'future_facture') else False,
        'periodicite': formdata['periodicite'],
        'date_debut': formdata['premiere_date'] if formdata['premiere_date'] != '' else None,
        'date_fin': formdata['date_fin'] if formdata['date_fin'] != '' else None,
    }

    # Crée ou met à jour l'objet facture
    if facture == None:
        fact = Facture.objects.create(**params)
    else:
        Facture.objects.filter(id=facture).update(**params)
        fact = Facture.objects.get(id=facture)

        # Efface les echeances liees à la facture
        Echeance.objects.filter(facture__id=facture).delete()

        # Efface les factures liees
        Facture.objects.filter(facture_liee__id=facture).delete()

    return fact

def creer_echeances(formdata, fact):

    if formdata['montant']=='':
        montant = 0
    else:
        montant = float(formdata['montant'].replace(',','.')) if formdata['type'] == 'emise' \
                    else -float(formdata['montant'].replace(',','.'))

    # Cree les echeances liées à la facture
    if formdata['periodicite'] == 'aucune':
        Echeance.objects.create(
            montant= montant,
            date_recouvrement=formdata['date_recouvrement'],
            facture=fact
        )
    else:
        dates = [formdata['premiere_date'], formdata['date_fin']]
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        delta = relativedelta(end, start)
        months = delta.months + delta.years * 12
        n = 1 if formdata['periodicite'] == 'mensuel' else 3
        for d in [start + relativedelta(months=x * n) for x in range(0, int(months / n) + 1)]:
            Echeance.objects.create(
                montant=montant / (int(months / n) + 1),
                date_recouvrement=d,
                facture=fact
            )

    return

def creer_facture_echeance_liees(formdata, fact, intitule):

    intit_emetteur = intitule
    intit_date = 'date_retro_' + intitule
    intit_montant = 'retrocession_' + intitule

    fact_com = Facture.objects.create(
        type='recue',
        #emetteur=getattr(formdata, intit_emetteur),
        emetteur=formdata[intit_emetteur],
        date_emission=formdata[intit_date],
        client=formdata['client'],
        future_facture=True,
        facture_liee=fact,
    )
    Echeance.objects.create(
        montant=-float(formdata[intit_montant].replace(',', '.')),
        date_recouvrement=formdata[intit_date],
        facture=fact_com
    )

    return
#
# def creer_fact_echeances(formdata, facture):
#
#     # Crée ou met à jour l'objet facture
#     if facture==None:
#         fact = Facture.objects.create(
#             type=formdata['type'],
#             emetteur=formdata['emetteur'],
#             client=formdata['client'],
#             #date_emission=datetime.strptime(formdata['date_emission'], '%d/%m/%Y').strftime('%Y-%m-%d'),
#             date_emission=formdata['date_emission'] if formdata['date_emission']!='' else None,
#             fichier=None if (not(hasattr(formdata, 'fichier')) or (formdata['fichier'] != '')) else formdata['fichier'],
#             future_facture=True if hasattr(formdata, 'future_facture') else False,
#             periodicite=formdata['periodicite'],
#             date_debut=formdata['premiere_date'],
#             date_fin=formdata['date_fin'],
#         )
#     else:
#         Facture.objects.filter(id=facture).update(
#             type=formdata['type'],
#             emetteur=formdata['emetteur'],
#             client=formdata['client'],
#             #date_emission=datetime.strptime(formdata['date_emission'], '%d/%m/%Y').strftime('%Y-%m-%d'),
#             date_emission=formdata['date_emission'] if formdata['date_emission']!='' else None,
#             fichier=None if (not(hasattr(formdata, 'fichier')) or (formdata['fichier'] != '')) else formdata['fichier'],
#             future_facture=True if hasattr(formdata, 'future_facture') else False,
#             periodicite=formdata['periodicite'],
#             date_debut=formdata['premiere_date'],
#             date_fin=formdata['date_fin'],
#         )
#         fact = Facture.objects.get(id=facture)
#
#         # Efface les echeances liees à la facture
#     Echeance.objects.filter(facture__id=facture).delete()
#
#     # Efface les factures liees
#     Facture.objects.filter(facture_liee__id=facture).delete()
#
#     # Cree les echeances liées à la facture
#     if formdata['periodicite'] == 'aucune':
#         Echeance.objects.create(
#             montant=float(formdata['montant'].replace(',','.')) if formdata['type'] == 'emise' \
#                 else -float(formdata['montant'].replace(',','.')),
#             date_recouvrement=formdata['date_recouvrement'],
#             facture=fact
#         )
#     else:
#         dates = [formdata['premiere_date'], formdata['date_fin']]
#         start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
#         delta = relativedelta(end, start)
#         months = delta.months + delta.years * 12
#         mt = float(formdata['montant'].replace(',','.') if formdata['type'] == 'emise' \
#                        else -float(formdata['montant'].replace(',','.')))
#         n = 1 if formdata['periodicite'] == 'mensuel' else 3
#         for d in [start + relativedelta(months=x * n) for x in range(0, int(months / n) + 1)]:
#             Echeance.objects.create(
#                 montant=mt / (int(months / n) + 1),
#                 date_recouvrement=d,
#                 facture=fact
#             )
#
#     # Si apporteur ou commercial, cree la facture secondaire et les echeances liées
#     if formdata['commercial'] != '':
#         fact_com = Facture.objects.create(
#             type='recue',
#             emetteur=formdata['commercial'],
#             date_emission=formdata['date_retro_commercial'],
#             client=formdata['client'],
#             future_facture=True,
#             facture_liee=fact,
#         )
#         Echeance.objects.create(
#             montant=-float(formdata['retrocession_commercial'].replace(',','.')),
#             date_recouvrement=formdata['date_retro_commercial'],
#             facture=fact_com
#         )
#     if formdata['commercial_2'] != '':
#         fact_com = Facture.objects.create(
#             type='recue',
#             emetteur=formdata['commercial_2'],
#             date_emission=formdata['date_retro_commercial_2'],
#             client=formdata['client'],
#             future_facture=True,
#             facture_liee=fact,
#         )
#         Echeance.objects.create(
#             montant=-float(formdata['retrocession_commercial_2'].replace(',','.')),
#             date_recouvrement=formdata['date_retro_commercial_2'],
#             facture=fact_com
#         )
#     if formdata['apporteur'] != '':
#         fact_app = Facture.objects.create(
#             type='recue',
#             emetteur=formdata['apporteur'],
#             date_emission=formdata['date_retro_apporteur'],
#             client=formdata['client'],
#             future_facture=True,
#             facture_liee=fact
#         )
#         Echeance.objects.create(
#             montant=-float(formdata['retrocession_apporteur'].replace(',','.')),
#             date_recouvrement=formdata['date_retro_apporteur'],
#             facture=fact_app
#         )
#
#     return