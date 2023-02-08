from django.contrib import admin
from django.urls import path

from comptabilite.facture.views import NouvelleFactureEmise, FactureCategorie, NouvelleFactureSimple, TestForm,\
    EcheancesView, echeances_vue, import_csv_factures

app_name = 'facture'

urlpatterns = [
    path('nouvelle/', NouvelleFactureEmise.as_view(), name='nouvelle_facture'),
    path('nouvelle_fact_categorie/', FactureCategorie.as_view(), name='nouvelle_fact_categorie'),
    path('nouvelle_fact_simple/', NouvelleFactureSimple.as_view(), name='nouvelle_fact_simple'),
    path('testform/', TestForm.as_view()),
    path('liste/', echeances_vue),
    path('liste/api/', EcheancesView.as_view()),
    path('import/', import_csv_factures),
#    path('postimport/', PostImport.as_view(), name='postimport')
]