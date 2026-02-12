from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Devis(models.Model):
    """Modèle pour les devis/factures"""

    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('paye', 'Payé'),
        ('annule', 'Annulé'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Numéro de devis")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    # Informations client
    client_nom = models.CharField(max_length=200, verbose_name="Nom du client")
    client_email = models.EmailField(blank=True, null=True, verbose_name="Email du client")
    client_telephone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Téléphone du client")
    client_adresse = models.TextField(blank=True, null=True, verbose_name="Adresse du client")

    # Statut et notes
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours', verbose_name="Statut")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes/Observations")

    # Mode de paiement
    MODE_PAIEMENT_CHOICES = [
        ('especes', 'Espèces'),
        ('mobile_money', 'Mobile Money'),
        ('carte', 'Carte bancaire'),
        ('virement', 'Virement'),
        ('cheque', 'Chèque'),
    ]
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES, blank=True, null=True, verbose_name="Mode de paiement")

    # Utilisateur qui a créé le devis
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='devis_crees', verbose_name="Créé par")

    class Meta:
        verbose_name = "Devis"
        verbose_name_plural = "Devis"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.numero} - {self.client_nom}"

    @property
    def total_fourniture(self):
        """Calcule le total des fournitures (somme des prix totaux des lignes)"""
        total = sum(ligne.prix_total for ligne in self.lignes.all())
        return Decimal(total)

    @property
    def main_oeuvre(self):
        """Calcule la main d'œuvre (25% du total fourniture)"""
        return self.total_fourniture * Decimal('0.25')

    @property
    def total_general(self):
        """Calcule le total général (Total Fourniture + Main d'œuvre)"""
        return self.total_fourniture + self.main_oeuvre

    def save(self, *args, **kwargs):
        # Générer automatiquement un numéro de devis si non fourni
        if not self.numero:
            from django.utils import timezone
            year = timezone.now().year
            count = Devis.objects.filter(date_creation__year=year).count() + 1
            self.numero = f"DEV-{year}-{count:04d}"
        super().save(*args, **kwargs)


class LigneDevis(models.Model):
    """Modèle pour les lignes d'un devis"""

    UNITE_CHOICES = [
        ('piece', 'Pièce'),
        ('m2', 'm²'),
        ('m3', 'm³'),
        ('kg', 'Kg'),
        ('tonne', 'Tonne'),
        ('litre', 'Litre'),
        ('metre', 'Mètre'),
        ('heure', 'Heure'),
        ('jour', 'Jour'),
        ('forfait', 'Forfait'),
    ]

    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name='lignes', verbose_name="Devis")
    numero_ligne = models.PositiveIntegerField(verbose_name="N°")
    libelle = models.CharField(max_length=500, verbose_name="Libellé")
    unite = models.CharField(max_length=20, choices=UNITE_CHOICES, default='piece', verbose_name="Unité")
    quantite = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Prix Unitaire (P.U)")

    class Meta:
        verbose_name = "Ligne de devis"
        verbose_name_plural = "Lignes de devis"
        ordering = ['numero_ligne']
        unique_together = ['devis', 'numero_ligne']

    def __str__(self):
        return f"{self.numero_ligne}. {self.libelle}"

    @property
    def prix_total(self):
        """Calcule le prix total (Quantité × Prix Unitaire)"""
        return self.quantite * self.prix_unitaire
