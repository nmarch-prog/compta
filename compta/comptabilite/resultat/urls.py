
from django.urls import path

from comptabilite.resultat.views import ResultatEntreDates

app_name = 'resultat'

urlpatterns = [
    path('dates/', ResultatEntreDates.as_view(), name='resultat-dates'),

]