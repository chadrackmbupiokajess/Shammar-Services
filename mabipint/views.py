from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from .models import Devis, LigneDevis
from .forms import DevisForm, LigneDevisForm
import json


def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'mabipint/login.html')


def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')


@login_required
def dashboard(request):
    """Tableau de bord principal"""
    devis_list = Devis.objects.all()[:10]

    # Statistiques
    total_devis = Devis.objects.count()
    devis_brouillon = Devis.objects.filter(statut='brouillon').count()
    devis_valide = Devis.objects.filter(statut='valide').count()
    devis_accepte = Devis.objects.filter(statut='accepte').count()

    context = {
        'devis_list': devis_list,
        'total_devis': total_devis,
        'devis_brouillon': devis_brouillon,
        'devis_valide': devis_valide,
        'devis_accepte': devis_accepte,
    }
    return render(request, 'mabipint/dashboard.html', context)


@login_required
def devis_list(request):
    """Liste de tous les devis"""
    devis_list = Devis.objects.all()
    return render(request, 'mabipint/devis_list.html', {'devis_list': devis_list})


@login_required
def devis_detail(request, pk):
    """Détail d'un devis"""
    devis = get_object_or_404(Devis, pk=pk)
    return render(request, 'mabipint/devis_detail.html', {'devis': devis})


@login_required
def devis_create(request):
    """Créer un nouveau devis"""
    if request.method == 'POST':
        form = DevisForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                devis = form.save(commit=False)
                devis.created_by = request.user
                devis.save()

                # Récupérer les lignes du formulaire (envoyées en JSON)
                lignes_data = request.POST.get('lignes_data')
                if lignes_data:
                    lignes = json.loads(lignes_data)
                    for ligne in lignes:
                        LigneDevis.objects.create(
                            devis=devis,
                            numero_ligne=ligne['numero'],
                            libelle=ligne['libelle'],
                            unite=ligne['unite'],
                            quantite=ligne['quantite'],
                            prix_unitaire=ligne['prix_unitaire']
                        )

                messages.success(request, f'Devis {devis.numero} créé avec succès!')
                return redirect('devis_detail', pk=devis.pk)
    else:
        form = DevisForm()

    return render(request, 'mabipint/devis_create.html', {'form': form})


@login_required
def devis_edit(request, pk):
    """Modifier un devis existant"""
    devis = get_object_or_404(Devis, pk=pk)

    if request.method == 'POST':
        form = DevisForm(request.POST, instance=devis)

        if form.is_valid():
            with transaction.atomic():
                devis = form.save()

                # Supprimer les anciennes lignes
                devis.lignes.all().delete()

                # Ajouter les nouvelles lignes
                lignes_data = request.POST.get('lignes_data')
                if lignes_data:
                    lignes = json.loads(lignes_data)
                    for ligne in lignes:
                        LigneDevis.objects.create(
                            devis=devis,
                            numero_ligne=ligne['numero'],
                            libelle=ligne['libelle'],
                            unite=ligne['unite'],
                            quantite=ligne['quantite'],
                            prix_unitaire=ligne['prix_unitaire']
                        )

                messages.success(request, f'Devis {devis.numero} modifié avec succès!')
                return redirect('devis_detail', pk=devis.pk)
    else:
        form = DevisForm(instance=devis)

    # Préparer les lignes existantes pour le JavaScript
    lignes_json = json.dumps([{
        'numero': ligne.numero_ligne,
        'libelle': ligne.libelle,
        'unite': ligne.unite,
        'quantite': str(ligne.quantite),
        'prix_unitaire': str(ligne.prix_unitaire)
    } for ligne in devis.lignes.all()])

    return render(request, 'mabipint/devis_edit.html', {
        'form': form,
        'devis': devis,
        'lignes_json': lignes_json
    })


@login_required
def devis_delete(request, pk):
    """Supprimer un devis"""
    devis = get_object_or_404(Devis, pk=pk)

    if request.method == 'POST':
        numero = devis.numero
        devis.delete()
        messages.success(request, f'Devis {numero} supprimé avec succès!')
        return redirect('devis_list')

    return render(request, 'mabipint/devis_delete.html', {'devis': devis})


@login_required
def devis_pdf(request, pk):
    """Générer un PDF du devis"""
    devis = get_object_or_404(Devis, pk=pk)

    # Pour l'instant, on affiche juste une version imprimable
    # On ajoutera la génération PDF avec ReportLab plus tard
    return render(request, 'mabipint/devis_pdf.html', {'devis': devis})
