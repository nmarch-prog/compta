from .models import Facture, Echeance
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

def creer_fact_echeances(formdata):

    # Crée l'objet facture
    fact = Facture.objects.create(
        type=formdata['type'],
        emetteur=formdata['emetteur_ou_client'],
        #date_emission=datetime.strptime(formdata['date_emission'], '%d/%m/%Y').strftime('%Y-%m-%d'),
        date_emission=formdata['date_emission'] if formdata['date_emission']!='' else None,
        fichier=None if (not(hasattr(formdata, 'fichier')) or (formdata['fichier'] != '')) else formdata['fichier'],
        future_facture=True if hasattr(formdata, 'future_facture') else False,
    )

    # Cree les echeances liées à la facture
    if formdata['periodicite'] == 'aucune':
        Echeance.objects.create(
            montant=float(formdata['montant'].replace(',','.')) if formdata['type'] == 'emise' \
                else -float(formdata['montant'].replace(',','.')),
            date_recouvrement=formdata['date_recouvrement'],
            facture=fact
        )
    else:
        dates = [formdata['premiere_date'], formdata['date_fin']]
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        delta = relativedelta(end, start)
        months = delta.months + delta.years * 12
        mt = float(formdata['montant'].replace(',','.') if formdata['type'] == 'emise' \
                       else -float(formdata['montant'].replace(',','.')))
        n = 1 if formdata['periodicite'] == 'mensuel' else 3
        for d in [start + relativedelta(months=x * n) for x in range(0, int(months / n) + 1)]:
            Echeance.objects.create(
                montant=mt / (int(months / n) + 1),
                date_recouvrement=d,
                facture=fact
            )

    # Si apporteur ou commercial, cree la facture secondaire et les echeances liées
    if formdata['commercial'] != '':
        fact_com = Facture.objects.create(
            type='recue',
            emetteur=formdata['commercial'],
            date_emission=formdata['date_retro_commercial'],
            future_facture=True,
        )
        Echeance.objects.create(
            montant=-formdata['retrocession_commercial'],
            date_recouvrement=formdata['date_retro_commercial'],
            facture=fact_com
        )
    if formdata['commercial_2'] != '':
        fact_com = Facture.objects.create(
            type='recue',
            emetteur=formdata['commercial_2'],
            date_emission=formdata['date_retro_commercial_2'],
            future_facture=True,
        )
        Echeance.objects.create(
            montant=-formdata['retrocession_commercial_2'],
            date_recouvrement=formdata['date_retro_commercial_2'],
            facture=fact_com
        )
    if formdata['apporteur'] != '':
        fact_app = Facture.objects.create(
            type='recue',
            emetteur=formdata['apporteur'],
            date_emission=formdata['date_retro_apporteur'],
            future_facture=True,
        )
        Echeance.objects.create(
            montant=-formdata['retrocession_apporteur'],
            date_recouvrement=formdata['date_retro_apporteur'],
            facture=fact_app
        )

    return