# 🔄 GUIDE DE MIGRATION - NOUVEAUX STATUTS

## SHAMMAR SERVICES - Écosystème MABIPINT

### ⚠️ IMPORTANT: Mise à Jour de la Base de Données

---

## 📋 CHANGEMENTS EFFECTUÉS

### Anciens Statuts → Nouveaux Statuts

| Ancien | Nouveau | Raison |
|--------|---------|--------|
| ~~Brouillon~~ | **En cours** | Plus adapté à la vente directe |
| ~~Validé~~ | ❌ Supprimé | Pas nécessaire pour vente directe |
| ~~Envoyé~~ | ❌ Supprimé | Pas de délai d'attente |
| ~~Accepté~~ | **Payé** | Client paie sur place |
| ~~Refusé~~ | **Annulé** | Vente non aboutie |

### Nouveaux Champs Ajoutés

- ✅ **mode_paiement** - Mode de paiement utilisé (Espèces, Mobile Money, etc.)

---

## 🚀 ÉTAPES DE MIGRATION

### 1️⃣ Créer les Migrations

Ouvrez PowerShell dans le dossier du projet et exécutez:

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate

# Créer les fichiers de migration
python manage.py makemigrations

# Vous devriez voir:
# Migrations for 'mabipint':
#   mabipint\migrations\0002_auto_XXXXXX.py
#     - Alter field statut on devis
#     - Add field mode_paiement to devis
```

### 2️⃣ Appliquer les Migrations

```powershell
# Appliquer les changements à la base de données
python manage.py migrate

# Vous devriez voir:
# Running migrations:
#   Applying mabipint.0002_auto_XXXXXX... OK
```

---

## ⚠️ GESTION DES DONNÉES EXISTANTES

### Si Vous Avez Déjà des Devis

Les anciens statuts seront **automatiquement convertis**:

| Ancien Statut | Converti en | Action Requise |
|---------------|-------------|----------------|
| `brouillon` | ⚠️ Invalide | Changer manuellement en `en_cours` |
| `valide` | ⚠️ Invalide | Changer manuellement en `en_cours` |
| `envoye` | ⚠️ Invalide | Changer manuellement en `paye` ou `annule` |
| `accepte` | ⚠️ Invalide | Changer manuellement en `paye` |
| `refuse` | ⚠️ Invalide | Changer manuellement en `annule` |

### Script de Conversion (Optionnel)

Si vous avez beaucoup de devis existants, créez ce script:

**Fichier:** `convert_statuts.py` (à la racine du projet)

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shammar_services.settings')
django.setup()

from mabipint.models import Devis

# Conversion des statuts
conversions = {
    'brouillon': 'en_cours',
    'valide': 'en_cours',
    'envoye': 'paye',
    'accepte': 'paye',
    'refuse': 'annule',
}

devis_list = Devis.objects.all()
count = 0

for devis in devis_list:
    if devis.statut in conversions:
        old_statut = devis.statut
        devis.statut = conversions[old_statut]
        devis.save()
        count += 1
        print(f"Devis {devis.numero}: {old_statut} → {devis.statut}")

print(f"\n✅ {count} devis convertis avec succès!")
```

**Exécuter le script:**

```powershell
python convert_statuts.py
```

---

## 🔧 ALTERNATIVE: BASE DE DONNÉES VIERGE

### Si Vous Préférez Repartir à Zéro

⚠️ **ATTENTION: Cela supprimera TOUTES vos données!**

```powershell
# 1. Supprimer la base de données
Remove-Item db.sqlite3

# 2. Supprimer les anciennes migrations (optionnel)
Remove-Item mabipint\migrations\0*.py

# 3. Recréer les migrations
python manage.py makemigrations

# 4. Créer la base de données
python manage.py migrate

# 5. Créer un nouveau super utilisateur
python manage.py createsuperuser
```

---

## ✅ VÉRIFICATION POST-MIGRATION

### 1. Tester la Création d'un Devis

```powershell
# Lancer le serveur
python manage.py runserver

# Aller sur http://127.0.0.1:8000/
# Créer un nouveau devis
# Vérifier que le statut par défaut est "En cours"
```

### 2. Vérifier les Statuts Disponibles

Dans le formulaire de création/modification, vous devriez voir:
- ✅ En cours
- ✅ Payé
- ✅ Annulé

### 3. Vérifier le Mode de Paiement

Le champ "Mode de paiement" devrait afficher:
- Espèces
- Mobile Money
- Carte bancaire
- Virement
- Chèque

---

## 🐛 RÉSOLUTION DE PROBLÈMES

### Erreur: "Invalid choice"

**Problème:** Les anciens statuts ne sont plus valides

**Solution:**
```powershell
# Option 1: Convertir avec le script
python convert_statuts.py

# Option 2: Via l'admin Django
# 1. Aller sur http://127.0.0.1:8000/admin/
# 2. Modifier chaque devis manuellement
# 3. Changer le statut vers un nouveau statut valide
```

### Erreur: "No such column: mode_paiement"

**Problème:** Migration non appliquée

**Solution:**
```powershell
python manage.py migrate
```

### Erreur: "Migrations are conflicting"

**Problème:** Conflit de migrations

**Solution:**
```powershell
# Supprimer les migrations conflictuelles
Remove-Item mabipint\migrations\0*.py

# Recréer les migrations
python manage.py makemigrations
python manage.py migrate
```

---

## 📊 APRÈS LA MIGRATION

### Nouvelles Fonctionnalités Disponibles

1. ✅ **Statuts simplifiés** (En cours, Payé, Annulé)
2. ✅ **Mode de paiement** sur chaque devis
3. ✅ **Workflow de vente directe** optimisé
4. ✅ **Protections adaptées** (seul "En cours" modifiable)
5. ✅ **Statistiques mises à jour** (En cours, Payés, Annulés)

### Dashboard Mis à Jour

Les cartes de statistiques affichent maintenant:
- 📊 Total Devis
- 🟠 En cours
- ✅ Payés
- ❌ Annulés

---

## 📝 CHECKLIST DE MIGRATION

Cochez au fur et à mesure:

- [ ] Sauvegarder la base de données actuelle (si nécessaire)
- [ ] Activer l'environnement virtuel
- [ ] Exécuter `python manage.py makemigrations`
- [ ] Exécuter `python manage.py migrate`
- [ ] Convertir les anciens statuts (si applicable)
- [ ] Tester la création d'un nouveau devis
- [ ] Vérifier les statuts disponibles
- [ ] Vérifier le champ mode de paiement
- [ ] Tester les protections (modification/suppression)
- [ ] Vérifier le dashboard
- [ ] Tester l'impression PDF
- [ ] Former les utilisateurs aux nouveaux statuts

---

## 🎓 FORMATION DES UTILISATEURS

### Points Clés à Communiquer

1. **Nouveaux statuts:**
   - 🟠 En cours (au lieu de Brouillon/Validé)
   - ✅ Payé (au lieu d'Accepté)
   - ❌ Annulé (au lieu de Refusé)

2. **Nouveau champ:**
   - Mode de paiement à sélectionner après paiement

3. **Workflow simplifié:**
   - Créer → Imprimer → Encaisser → Marquer comme Payé

4. **Protection:**
   - Seuls les devis "En cours" sont modifiables

---

## 📞 SUPPORT

En cas de problème lors de la migration:

1. Vérifier les messages d'erreur
2. Consulter ce guide
3. Contacter l'administrateur système

---

## ✅ MIGRATION RÉUSSIE!

Une fois toutes les étapes complétées, votre application est prête pour la vente directe!

**Bonne utilisation! 🚀**
