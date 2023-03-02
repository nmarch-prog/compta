from django.contrib import admin
from django.urls import path

from comptabilite.ecriture.views import ImportEcrituresCsv
from comptabilite.element_comptable.views import EcrituresNonComptabiliseesView, ComptaMensuelleView

app_name = 'element_comptable'

urlpatterns = [
    path('import_csv/', ImportEcrituresCsv.as_view(), name='import'),
    path('cat_ecritures/', EcrituresNonComptabiliseesView.as_view(), name='cat_ecriture'),
    path('comptes/<str:mois>/', ComptaMensuelleView.as_view(), name='compta_mensuelle')
#    path('')
#    path('postimport/', PostImport.as_view(), name='postimport')
]