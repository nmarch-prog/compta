from django.contrib import admin
from django.urls import path

from comptabilite.ecriture.views import ImportEcrituresCsv, ImportEcrituresCategoriesCsv

app_name = 'ecriture'

urlpatterns = [
    path('import_csv/', ImportEcrituresCsv.as_view(), name='import'),
    path('import_csv_categories/', ImportEcrituresCategoriesCsv.as_view(), name='import_categories'),
]