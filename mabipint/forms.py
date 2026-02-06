from django import forms
from .models import Devis, LigneDevis


class DevisForm(forms.ModelForm):
    """Formulaire pour créer/modifier un devis"""

    class Meta:
        model = Devis
        fields = ['client_nom', 'client_email', 'client_telephone', 'client_adresse', 'statut', 'notes']
        widgets = {
            'client_nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nom complet du client'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'email@exemple.com'
            }),
            'client_telephone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '+243 XXX XXX XXX'
            }),
            'client_adresse': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Adresse complète du client',
                'rows': 3
            }),
            'statut': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Notes ou observations supplémentaires',
                'rows': 4
            }),
        }


class LigneDevisForm(forms.ModelForm):
    """Formulaire pour une ligne de devis"""

    class Meta:
        model = LigneDevis
        fields = ['numero_ligne', 'libelle', 'unite', 'quantite', 'prix_unitaire']
        widgets = {
            'numero_ligne': forms.NumberInput(attrs={
                'class': 'w-20 px-2 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-center',
                'min': '1'
            }),
            'libelle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Description de l\'article'
            }),
            'unite': forms.Select(attrs={
                'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'quantite': forms.NumberInput(attrs={
                'class': 'w-32 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01',
                'min': '0'
            }),
            'prix_unitaire': forms.NumberInput(attrs={
                'class': 'w-32 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'step': '0.01',
                'min': '0'
            }),
        }
