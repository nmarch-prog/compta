"""CRM_AFPI78 URL Configuration

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

from django.urls import path

from utilisateurs.views import BaseView, ListeUtilisateurs, CreerCollaborateur, EditerCollaborateur, \
    SupprimerCollaborateur, CreerCourtier, EditerCourtier, SupprimerCourtier


app_name = 'utilisateurs'

urlpatterns = [
    path('', BaseView.as_view()),
    path('liste/', ListeUtilisateurs.as_view(), name='liste'),
    path('collaborateur/creer/', CreerCollaborateur.as_view(), name='creer-collab'),
    path('collaborateur/<str:pk>/editer/', EditerCollaborateur.as_view(), name='editer-collab'),
    path('collaborateur/<str:pk>/supprimer/', SupprimerCollaborateur.as_view(), name='supprimer-collab'),
    path('courtier/creer/', CreerCourtier.as_view(), name='creer-courtier'),
    path('courtier/<str:pk>/editer/', EditerCourtier.as_view(), name='editer-courtier'),
    path('courtier/<str:pk>/supprimer/', SupprimerCollaborateur.as_view(), name='supprimer-courtier'),
]


