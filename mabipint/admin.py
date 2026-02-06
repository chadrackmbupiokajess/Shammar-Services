from django.contrib import admin
from .models import Devis, LigneDevis


class LigneDevisInline(admin.TabularInline):
    model = LigneDevis
    extra = 1
    fields = ['numero_ligne', 'libelle', 'unite', 'quantite', 'prix_unitaire']


@admin.register(Devis)
class DevisAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client_nom', 'date_creation', 'statut', 'total_general']
    list_filter = ['statut', 'date_creation']
    search_fields = ['numero', 'client_nom', 'client_email']
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
        if not change:  # Si c'est une nouvelle création
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(LigneDevis)
class LigneDevisAdmin(admin.ModelAdmin):
    list_display = ['devis', 'numero_ligne', 'libelle', 'quantite', 'unite', 'prix_unitaire', 'prix_total']
    list_filter = ['devis', 'unite']
    search_fields = ['libelle', 'devis__numero']
