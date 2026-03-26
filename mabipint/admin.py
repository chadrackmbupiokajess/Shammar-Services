from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Devis, LigneDevis


class LigneDevisInline(admin.TabularInline):
    model = LigneDevis
    extra = 1
    fields = ['numero_ligne', 'libelle', 'unite', 'quantite', 'prix_unitaire']


@admin.register(Devis)
class DevisAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client_nom', 'date_creation', 'statut', 'total_general', 'created_by']
    list_filter = ['statut', 'date_creation', 'created_by']
    search_fields = ['numero', 'client_nom', 'client_email', 'created_by__username']
    readonly_fields = ['date_creation', 'date_modification', 'created_by']
    inlines = [LigneDevisInline]

    fieldsets = (
        ('Informations du devis', {
            'fields': ('numero', 'statut', 'created_by', 'date_creation', 'date_modification')
        }),
        ('Informations client', {
            'fields': ('client_nom', 'client_email', 'client_telephone', 'client_adresse')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(LigneDevis)
class LigneDevisAdmin(admin.ModelAdmin):
    list_display = ['devis', 'numero_ligne', 'libelle', 'quantite', 'unite', 'prix_unitaire', 'prix_total']
    list_filter = ['devis', 'unite']
    search_fields = ['libelle', 'devis__numero']


# Dé-enregistrer l'UserAdmin par défaut
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('total_ventes', 'chiffre_affaires_total')

    def total_ventes(self, obj):
        # Compte le nombre de ventes créées par cet utilisateur
        return obj.devis_crees.count()
    total_ventes.short_description = 'Nombre de Ventes'

    def chiffre_affaires_total(self, obj):
        # Calcule la somme des totaux généraux de ses ventes
        ventes = obj.devis_crees.all()
        total = sum(v.total_general for v in ventes)
        return f"{total:,.0f} FC"
    chiffre_affaires_total.short_description = 'CA Total'
