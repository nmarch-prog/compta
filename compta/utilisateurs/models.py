from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    pass


class Collaborateur(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    droit_gestion_utilisateurs = models.BooleanField(null=True, blank=True)
    droit_comptabilite = models.BooleanField(null=True, blank=True)
    droit_suivi_clients = models.BooleanField(null=True, blank=True)
    statut = models.CharField(max_length=10, choices=[('Employe', 'Employe'), ('Mandataire', 'Mandataire'),
                                                      ('Gerant', 'Gerant')])


class Courtier(models.Model):

   def __str__(self):
       return self.collaborateur.user.username


   collaborateur = models.OneToOneField(Collaborateur, on_delete=models.CASCADE)
   zone = models.CharField(max_length=10, choices=[('bleue', 'bleue'), ('verte', 'verte'), ('jaune', 'jaune'),
                                                  ('rose', 'rose')], null=True, blank=True)