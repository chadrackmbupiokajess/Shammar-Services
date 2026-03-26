from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Devis, LigneDevis
from .forms import DevisForm, LigneDevisForm
import json
from decimal import Decimal
from django.db.models import Sum
from django.core.paginator import Paginator


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
    now = timezone.now()
    
    # Récupérer la date de filtrage si elle existe
    date_filter_str = request.GET.get('date_filter')
    if date_filter_str:
        try:
            target_date = datetime.strptime(date_filter_str, '%Y-%m-%d').date()
            # On crée un datetime à partir de la date pour les calculs
            reference_date = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))
        except ValueError:
            reference_date = now
    else:
        reference_date = now

    # Statistiques de base (toujours globales)
    total_devis = Devis.objects.count()
    devis_paye = Devis.objects.filter(statut='paye').count()

    # Chiffre d'affaires total
    toutes_les_ventes = Devis.objects.all()
    chiffre_affaires_total = sum(v.total_general for v in toutes_les_ventes)

    # Chiffre d'affaires par période
    # Aujourd'hui
    ventes_aujourdhui = Devis.objects.filter(date_creation__date=now.date())
    ca_aujourdhui = sum(v.total_general for v in ventes_aujourdhui)

    # Cette semaine
    debut_semaine = now - timedelta(days=now.weekday())
    ventes_semaine = Devis.objects.filter(date_creation__gte=debut_semaine)
    ca_semaine = sum(v.total_general for v in ventes_semaine)

    # Ce mois-ci
    ventes_mois = Devis.objects.filter(date_creation__month=now.month, date_creation__year=now.year)
    ca_mois = sum(v.total_general for v in ventes_mois)

    # Cette année
    ventes_annee = Devis.objects.filter(date_creation__year=now.year)
    ca_annee = sum(v.total_general for v in ventes_annee)

    # Données pour le graphique (7 jours à partir de la date de référence)
    graph_labels = []
    graph_data = []
    for i in range(6, -1, -1):
        day = reference_date - timedelta(days=i)
        graph_labels.append(day.strftime('%d/%m'))
        ventes_jour = Devis.objects.filter(date_creation__date=day.date())
        total_jour = sum(v.total_general for v in ventes_jour)
        graph_data.append(float(total_jour))

    context = {
        'devis_list': devis_list,
        'total_devis': total_devis,
        'devis_paye': devis_paye,
        'chiffre_affaires_total': chiffre_affaires_total,
        'ca_aujourdhui': ca_aujourdhui,
        'ca_semaine': ca_semaine,
        'ca_mois': ca_mois,
        'ca_annee': ca_annee,
        'graph_labels': json.dumps(graph_labels),
        'graph_data': json.dumps(graph_data),
        'date_filter_val': date_filter_str or now.strftime('%Y-%m-%d'),
    }
    return render(request, 'mabipint/dashboard.html', context)


@login_required
def devis_list(request):
    """Liste de tous les devis avec pagination et recherche AJAX"""
    devis_queryset = Devis.objects.all().order_by('-date_creation')
    
    # Paramètre de recherche
    search_query = request.GET.get('search')
    if search_query:
        from django.db.models import Q
        devis_queryset = devis_queryset.filter(
            Q(numero__icontains=search_query) |
            Q(client_nom__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(devis_queryset, 10)
    page_number = request.GET.get('page')
    devis_list = paginator.get_page(page_number)
    
    context = {
        'devis_list': devis_list,
        'search_query': search_query
    }
    
    # Si c'est une requête AJAX, on renvoie juste le tableau partiel
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'mabipint/partials/devis_table_partial.html', context)

    return render(request, 'mabipint/devis_list.html', context)


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
