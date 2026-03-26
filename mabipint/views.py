from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse, Http404
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
    """Tableau de bord principal (Filtré par rôle)"""
    # Si superutilisateur, voir tout. Sinon, voir uniquement ses propres ventes.
    if request.user.is_superuser:
        user_devis = Devis.objects.all()
    else:
        user_devis = Devis.objects.filter(created_by=request.user)
        
    devis_list = user_devis.order_by('-date_creation')[:10]
    now = timezone.now()
    
    # Récupérer la date de filtrage si elle existe
    date_filter_str = request.GET.get('date_filter')
    if date_filter_str:
        try:
            target_date = datetime.strptime(date_filter_str, '%Y-%m-%d').date()
            reference_date = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))
        except ValueError:
            reference_date = now
    else:
        reference_date = now

    # Statistiques de base
    total_devis = user_devis.count()
    devis_paye = user_devis.filter(statut='paye').count()

    # Chiffre d'affaires total
    chiffre_affaires_total = sum(v.total_general for v in user_devis)

    # Chiffre d'affaires par période
    # Aujourd'hui
    ca_aujourdhui = sum(v.total_general for v in user_devis.filter(date_creation__date=now.date()))

    # Cette semaine
    debut_semaine = now - timedelta(days=now.weekday())
    ca_semaine = sum(v.total_general for v in user_devis.filter(date_creation__gte=debut_semaine))

    # Ce mois-ci
    ca_mois = sum(v.total_general for v in user_devis.filter(date_creation__month=now.month, date_creation__year=now.year))

    # Cette année
    ca_annee = sum(v.total_general for v in user_devis.filter(date_creation__year=now.year))

    # Données pour le graphique
    graph_labels = []
    graph_data = []
    for i in range(6, -1, -1):
        day = reference_date - timedelta(days=i)
        graph_labels.append(day.strftime('%d/%m'))
        ventes_jour = user_devis.filter(date_creation__date=day.date())
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
    """Liste de tous les devis (Filtrée par rôle) avec pagination et recherche AJAX"""
    if request.user.is_superuser:
        devis_queryset = Devis.objects.all().order_by('-date_creation')
    else:
        devis_queryset = Devis.objects.filter(created_by=request.user).order_by('-date_creation')
    
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
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'mabipint/partials/devis_table_partial.html', context)

    return render(request, 'mabipint/devis_list.html', context)


@login_required
def devis_detail(request, pk):
    """Détail d'un devis (Sécurisé par rôle)"""
    devis = get_object_or_404(Devis, pk=pk)
    # Sécurité : vérifier que le devis appartient à l'utilisateur OU que l'utilisateur est admin
    if not request.user.is_superuser and devis.created_by != request.user:
        raise Http404("Vous n'avez pas l'autorisation de voir cette vente.")
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
    """Modifier un devis existant (Sécurisé par rôle)"""
    devis = get_object_or_404(Devis, pk=pk)
    # Sécurité : Admin peut tout modifier, sinon seulement ses propres ventes
    if not request.user.is_superuser and devis.created_by != request.user:
        raise Http404("Modification interdite.")

    if request.method == 'POST':
        form = DevisForm(request.POST, instance=devis)

        if form.is_valid():
            with transaction.atomic():
                devis = form.save()
                devis.lignes.all().delete()

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
    """Supprimer un devis (Sécurisé par rôle)"""
    devis = get_object_or_404(Devis, pk=pk)
    # Sécurité
    if not request.user.is_superuser and devis.created_by != request.user:
        raise Http404("Suppression interdite.")

    if request.method == 'POST':
        numero = devis.numero
        devis.delete()
        messages.success(request, f'Vente {numero} supprimée avec succès!')
        return redirect('devis_list')

    return render(request, 'mabipint/devis_delete.html', {'devis': devis})


@login_required
def devis_pdf(request, pk):
    """Générer un PDF du devis (Sécurisé par rôle)"""
    devis = get_object_or_404(Devis, pk=pk)
    # Sécurité
    if not request.user.is_superuser and devis.created_by != request.user:
        raise Http404("Visualisation interdite.")

    return render(request, 'mabipint/devis_pdf.html', {'devis': devis})


@login_required
def aide_statuts(request):
    """Page d'aide sur les statuts"""
    return render(request, 'mabipint/aide_statuts.html')
