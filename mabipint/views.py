from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Devis, LigneDevis, UserProfile
from .forms import DevisForm, LigneDevisForm, UserCreateForm, UserEditForm
import json
from decimal import Decimal
from django.db.models import Sum, Q
from django.core.paginator import Paginator


# --- Gestion des Sessions Services ---

def get_current_service(request):
    """Récupère le service actif en session pour tous les utilisateurs."""
    return request.session.get('current_service', 'mabipeint')

@login_required
def switch_service(request, service_name):
    """Permet à tous les utilisateurs authentifiés de changer de service."""
    if service_name in ['mabipeint', 'cleaning']:
        request.session['current_service'] = service_name
        messages.success(request, f"Système basculé vers {service_name.upper()}.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


# --- Authentification ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            request.session['current_service'] = profile.default_service
            messages.success(request, f'Bienvenue {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants incorrects.')

    return render(request, 'mabipint/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# --- Dashboard ---

@login_required
def dashboard(request):
    service = get_current_service(request)
    
    # FILTRAGE : Admin voit TOUT, Utilisateur voit SEULEMENT SES activités
    if request.user.is_superuser:
        user_devis = Devis.objects.filter(service=service)
    else:
        user_devis = Devis.objects.filter(service=service, created_by=request.user)
        
    # Gestion du filtre de date pour le graphique
    date_filter = request.GET.get('date_filter')
    if date_filter:
        try:
            target_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
        except ValueError:
            target_date = timezone.now().date()
    else:
        target_date = timezone.now().date()

    # Statistiques basées sur le filtrage ci-dessus
    total_devis = user_devis.count()
    devis_paye = user_devis.filter(statut='paye').count()
    chiffre_affaires_total = sum(v.total_general for v in user_devis)

    # Calcul des recettes temporelles
    now = timezone.now()
    ca_aujourdhui = sum(v.total_general for v in user_devis.filter(date_creation__date=now.date()))
    ca_semaine = sum(v.total_general for v in user_devis.filter(date_creation__gte=now-timedelta(days=7)))
    ca_mois = sum(v.total_general for v in user_devis.filter(date_creation__month=now.month, date_creation__year=now.year))
    ca_annee = sum(v.total_general for v in user_devis.filter(date_creation__year=now.year))

    # Préparation des données du graphique
    graph_labels = []
    graph_data = []
    for i in range(6, -1, -1):
        day = target_date - timedelta(days=i)
        graph_labels.append(day.strftime('%d/%m/%Y'))
        ventes_jour = user_devis.filter(date_creation__date=day)
        graph_data.append(float(sum(v.total_general for v in ventes_jour)))

    context = {
        'service': service,
        'devis_list': user_devis.order_by('-date_creation')[:10],
        'total_devis': total_devis,
        'devis_paye': devis_paye,
        'chiffre_affaires_total': chiffre_affaires_total,
        'ca_aujourdhui': ca_aujourdhui,
        'ca_semaine': ca_semaine,
        'ca_mois': ca_mois,
        'ca_annee': ca_annee,
        'graph_labels': json.dumps(graph_labels),
        'graph_data': json.dumps(graph_data),
        'date_filter_val': target_date.strftime('%Y-%m-%d'),
        'now': now,
    }
    return render(request, 'mabipint/dashboard.html', context)


# --- Utilisateurs ---

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    service = get_current_service(request)
    search_query = request.GET.get('search', '')
    users = User.objects.all()
    
    if search_query:
        users = users.filter(Q(username__icontains=search_query) | Q(first_name__icontains=search_query))
    
    user_data = []
    for user in users:
        ventes = Devis.objects.filter(created_by=user, service=service)
        user_data.append({
            'user': user,
            'total_ventes': ventes.count(),
            'ca_total': sum(v.total_general for v in ventes)
        })
    
    return render(request, 'mabipint/user_list.html', {'user_data': user_data, 'service': service})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                UserProfile.objects.create(user=user, telephone=form.cleaned_data['telephone'])
                messages.success(request, f"L'agent {user.username} a été ajouté.")
                return redirect('user_list')
    else: form = UserCreateForm()
    return render(request, 'mabipint/user_create.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_edit(request, pk):
    user_to_edit = get_object_or_404(User, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=user_to_edit)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                profile.telephone = form.cleaned_data['telephone']
                profile.save()
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                messages.success(request, "Informations mises à jour.")
                return redirect('user_list')
    else: 
        form = UserEditForm(instance=user_to_edit, initial={'telephone': profile.telephone})
    return render(request, 'mabipint/user_edit.html', {'form': form, 'user_to_edit': user_to_edit})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    u = get_object_or_404(User, pk=pk)
    if u != request.user: u.delete()
    return redirect('user_list')


# --- Ventes ---

@login_required
def devis_list(request):
    service = get_current_service(request)
    # FILTRAGE : Admin voit TOUT, Utilisateur voit SEULEMENT SES ventes
    if request.user.is_superuser:
        devis_queryset = Devis.objects.filter(service=service).order_by('-date_creation')
    else:
        devis_queryset = Devis.objects.filter(service=service, created_by=request.user).order_by('-date_creation')
    
    search = request.GET.get('search')
    if search:
        devis_queryset = devis_queryset.filter(Q(numero__icontains=search) | Q(client_nom__icontains=search))
    
    paginator = Paginator(devis_queryset, 10)
    devis_list = paginator.get_page(request.GET.get('page'))
    
    context = {'devis_list': devis_list, 'search_query': search, 'service': service}
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'mabipint/partials/devis_table_partial.html', context)
    return render(request, 'mabipint/devis_list.html', context)

@login_required
def devis_create(request):
    service = get_current_service(request)
    if request.method == 'POST':
        form = DevisForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                devis = form.save(commit=False)
                devis.created_by = request.user
                devis.service = service
                devis.save()

                lignes_data = request.POST.get('lignes_data')
                if lignes_data:
                    for ligne in json.loads(lignes_data):
                        LigneDevis.objects.create(
                            devis=devis, numero_ligne=ligne['numero'], libelle=ligne['libelle'],
                            unite=ligne['unite'], quantite=ligne['quantite'], prix_unitaire=ligne['prix_unitaire']
                        )
                messages.success(request, f'Enregistrement {devis.numero} réussi!')
                return redirect('devis_detail', pk=devis.pk)
    else: form = DevisForm()
    return render(request, 'mabipint/devis_create.html', {'form': form, 'service': service})

@login_required
def devis_detail(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    # PROTECTION : Un agent ne peut pas voir les détails d'un autre agent
    if not request.user.is_superuser and devis.created_by != request.user:
        raise Http404()
    return render(request, 'mabipint/devis_detail.html', {'devis': devis})

@login_required
def devis_edit(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    # PROTECTION : Un agent ne peut pas modifier la vente d'un autre agent
    if not request.user.is_superuser and devis.created_by != request.user:
        raise Http404()
        
    if request.method == 'POST':
        form = DevisForm(request.POST, instance=devis)
        if form.is_valid():
            with transaction.atomic():
                devis = form.save()
                devis.lignes.all().delete()
                lignes_data = request.POST.get('lignes_data')
                if lignes_data:
                    for ligne in json.loads(lignes_data):
                        LigneDevis.objects.create(
                            devis=devis, numero_ligne=ligne['numero'], libelle=ligne['libelle'],
                            unite=ligne['unite'], quantite=ligne['quantite'], prix_unitaire=ligne['prix_unitaire']
                        )
                messages.success(request, "Modifié.")
                return redirect('devis_detail', pk=devis.pk)
    else: form = DevisForm(instance=devis)
    lignes_json = json.dumps([{'numero': l.numero_ligne, 'libelle': l.libelle, 'unite': l.unite, 'quantite': str(l.quantite), 'prix_unitaire': str(l.prix_unitaire)} for l in devis.lignes.all()])
    return render(request, 'mabipint/devis_edit.html', {
        'form': form, 
        'devis': devis, 
        'lignes_json': lignes_json,
        'service': devis.service
    })

@login_required
def devis_delete(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    # PROTECTION : Un agent ne peut pas supprimer la vente d'un autre agent
    if not request.user.is_superuser and devis.created_by != request.user:
        raise Http404()
    devis.delete()
    return redirect('devis_list')

@login_required
def devis_pdf(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    # PROTECTION : Un agent ne peut pas générer le PDF d'un autre agent
    if not request.user.is_superuser and devis.created_by != request.user:
        raise Http404()
    return render(request, 'mabipint/devis_pdf.html', {'devis': devis})

@login_required
def aide_statuts(request):
    service = get_current_service(request)
    return render(request, 'mabipint/aide_statuts.html', {'service': service})
