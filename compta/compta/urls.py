"""compta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from afpi_import_csv.views import ImportCsvView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ecritures/', include('comptabilite.ecriture.urls', namespace='ecriture')),
    path('factures/', include('comptabilite.facture.urls', namespace='facture')),
    path('element_comptable/', include('comptabilite.element_comptable.urls', namespace='element_comptable')),
    path('resultat/', include('comptabilite.resultat.urls', namespace='resultat')),
    path('import_csv/', ImportCsvView.as_view(), name='import_csv'),

]
