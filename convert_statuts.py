"""
Script de conversion des anciens statuts vers les nouveaux statuts
Pour SHAMMAR SERVICES - Écosystème MABIPINT

Exécuter avec: python convert_statuts.py
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shammar_services.settings')
django.setup()

from mabipint.models import Devis

def convert_statuts():
    """Convertir les anciens statuts vers les nouveaux"""

    # Mapping des conversions
    conversions = {
        'brouillon': 'en_cours',
        'valide': 'en_cours',
        'envoye': 'paye',
        'accepte': 'paye',
        'refuse': 'annule',
    }

    print("=" * 60)
    print("CONVERSION DES STATUTS - SHAMMAR SERVICES")
    print("=" * 60)
    print()

    # Récupérer tous les devis
    devis_list = Devis.objects.all()
    total = devis_list.count()

    if total == 0:
        print("✅ Aucun devis à convertir.")
        return

    print(f"📊 {total} devis trouvés dans la base de données")
    print()

    # Compteurs
    converted = 0
    already_ok = 0

    # Conversion
    for devis in devis_list:
        if devis.statut in conversions:
            old_statut = devis.statut
            new_statut = conversions[old_statut]
            devis.statut = new_statut
            devis.save()
            converted += 1
            print(f"✅ Devis {devis.numero}: {old_statut} → {new_statut}")
        elif devis.statut in ['en_cours', 'paye', 'annule']:
            already_ok += 1
            print(f"ℹ️  Devis {devis.numero}: {devis.statut} (déjà à jour)")
        else:
            print(f"⚠️  Devis {devis.numero}: statut inconnu '{devis.statut}'")

    # Résumé
    print()
    print("=" * 60)
    print("RÉSUMÉ DE LA CONVERSION")
    print("=" * 60)
    print(f"Total de devis:        {total}")
    print(f"Convertis:             {converted}")
    print(f"Déjà à jour:           {already_ok}")
    print()

    if converted > 0:
        print(f"✅ {converted} devis convertis avec succès!")
    else:
        print("✅ Tous les devis sont déjà à jour!")

    print()
    print("🎉 Conversion terminée!")
    print()


if __name__ == '__main__':
    try:
        convert_statuts()
    except Exception as e:
        print()
        print("❌ ERREUR lors de la conversion:")
        print(f"   {str(e)}")
        print()
        print("💡 Assurez-vous que:")
        print("   1. L'environnement virtuel est activé")
        print("   2. Les migrations ont été appliquées (python manage.py migrate)")
        print("   3. La base de données existe")
        print()
