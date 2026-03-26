from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from .models import Devis, LigneDevis
from .forms import DevisForm, LigneDevisForm
import json
from decimal import Decimal


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
    devis_paye = Devis.objects.filter(statut='paye').count()

    # Calcul du chiffre d'affaires total
    # Comme on a des propriétés calculées dans le modèle, on doit boucler sur les objets
    toutes_les_ventes = Devis.objects.all()
    chiffre_affaires_total = sum(v.total_general for v in toutes_les_ventes)

    context = {
        'devis_list': devis_list,
        'total_devis': total_devis,
        'devis_paye': devis_paye,
        'chiffre_affaires_total': chiffre_affaires_total,
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

                messages.success(request, f'Vente {devis.numero} enregistrée avec succès!')
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

                messages.success(request, f'Vente {devis.numero} modifiée avec succès!')
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
        messages.success(request, f'Vente {numero} supprimée avec succès!')
        return redirect('devis_list')

    return render(request, 'mabipint/devis_delete.html', {'devis': devis})


@login_required
def devis_pdf(request, pk):
    """Générer un PDF du devis"""
    devis = get_object_or_404(Devis, pk=pk)

    # Pour l'instant, on affiche juste une version imprimable
    # On ajoutera la génération PDF avec ReportLab plus tard
    return render(request, 'mabipint/devis_pdf.html', {'devis': devis})


@login_required
def aide_statuts(request):
    """Page d'aide sur les statuts"""
    return render(request, 'mabipint/aide_statuts.html')
