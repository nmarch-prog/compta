from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, TemplateView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm, PasswordChangeForm, SetPasswordForm
from .forms import CollaborateurModelForm, CourtierModelForm
from .models import Collaborateur, User
from apporteurs.models import Courtier

# Create your views here.

class BaseView(LoginRequiredMixin,TemplateView):
    template_name = 'base_utilisateurs.html'


class ListeUtilisateurs(LoginRequiredMixin, ListView):
    queryset = User.objects.all()
    template_name = 'liste_utilisateurs.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['collaborateurs'] = Collaborateur.objects.all()
        context['courtiers'] = Courtier.objects.all()
        return context


class CreerCollaborateur(LoginRequiredMixin, CreateView):
    template_name = 'creer_utilisateur.html'
    form_class = CollaborateurModelForm
    success_url = reverse_lazy('utilisateurs:liste')


class EditerCollaborateur(LoginRequiredMixin, UpdateView):
    template_name = 'creer_utilisateur.html'
    queryset = Collaborateur.objects.all()
    form_class = CollaborateurModelForm
    success_url = reverse_lazy('utilisateurs:liste')


class SupprimerCollaborateur(LoginRequiredMixin, DeleteView):
    template_name = 'supprimer_utilisateur.html'
    queryset = Collaborateur.objects.all()
    success_url = reverse_lazy('utilisateurs:liste')


class CreerCourtier(LoginRequiredMixin, CreateView):
    template_name = 'creer_utilisateur.html'
    form_class = CourtierModelForm
    success_url = reverse_lazy('utilisateurs:liste')


class EditerCourtier(LoginRequiredMixin, UpdateView):
    template_name = 'creer_utilisateur.html'
    queryset = Courtier.objects.all()
    form_class = CourtierModelForm
    success_url = reverse_lazy('utilisateurs:liste')


class SupprimerCourtier(LoginRequiredMixin, DeleteView):
    template_name = 'supprimer_utilisateur.html'
    queryset = Courtier.objects.all()
    success_url = reverse_lazy('utilisateurs:liste')
