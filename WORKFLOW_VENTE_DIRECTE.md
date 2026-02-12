# 🛒 WORKFLOW DE VENTE DIRECTE

## SHAMMAR SERVICES - Écosystème MABIPINT

### ✅ Application Adaptée pour la Vente Directe

---

## 🎯 CONCEPT

Cette application est conçue pour un **système de vente directe** où:
- Le client vient au magasin/bureau
- Vous créez le devis sur place
- Vous imprimez la facture immédiatement
- Le client paie et repart avec sa facture

**Ce n'est PAS** un système où le client accepte/refuse plus tard!

---

## 📊 LES 3 STATUTS

### 1. 🟠 **EN COURS** (Statut par défaut)

**Utilisation:**
- Devis en cours de création
- Client présent, vous ajoutez les articles
- Calculs en temps réel

**Actions possibles:**
- ✅ Modifier librement
- ✅ Ajouter/Supprimer des lignes
- ✅ Supprimer le devis
- ✅ Changer le statut

**Badge:** Orange avec icône horloge ⏰

---

### 2. ✅ **PAYÉ** (Vente finalisée)

**Utilisation:**
- Client a payé
- Facture imprimée et remise
- Transaction terminée

**Actions possibles:**
- ❌ Modification verrouillée 🔒
- ❌ Suppression verrouillée 🚫
- ✅ Visualisation
- ✅ Réimpression

**Badge:** Vert avec icône billet 💵

**Protection:**
> Une fois payé, le devis est verrouillé pour garantir l'intégrité de la transaction.

---

### 3. ❌ **ANNULÉ** (Vente non aboutie)

**Utilisation:**
- Client a changé d'avis
- Produit non disponible
- Erreur de saisie à supprimer

**Actions possibles:**
- ❌ Modification verrouillée 🔒
- ✅ Suppression autorisée
- ✅ Visualisation

**Badge:** Rouge avec icône croix ✖️

---

## 💳 MODES DE PAIEMENT

L'application supporte 5 modes de paiement:

1. 💵 **Espèces** - Paiement en cash
2. 📱 **Mobile Money** - M-Pesa, Orange Money, Airtel Money, etc.
3. 💳 **Carte bancaire** - Paiement par carte
4. 🏦 **Virement** - Virement bancaire
5. 📝 **Chèque** - Paiement par chèque

---

## 🔄 PROCESSUS DE VENTE STANDARD

### Étape par Étape

```
┌─────────────────────────────────────────┐
│  1. CLIENT ARRIVE AU MAGASIN            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  2. CRÉER NOUVEAU DEVIS                 │
│     → Statut: EN COURS (automatique)    │
│     → Saisir nom du client              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  3. AJOUTER LES ARTICLES                │
│     → Cliquer "Ajouter une ligne"       │
│     → Saisir: Libellé, Qté, P.U         │
│     → Totaux calculés automatiquement   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  4. VÉRIFIER LES TOTAUX                 │
│     → Total Fourniture                  │
│     → M.O (25%)                         │
│     → Total Général                     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  5. ENREGISTRER LE DEVIS                │
│     → Cliquer "Enregistrer"             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  6. IMPRIMER LA FACTURE                 │
│     → Cliquer "Voir PDF"                │
│     → Cliquer "Imprimer"                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  7. CLIENT PAIE                         │
│     → Recevoir le paiement              │
│     → Sélectionner mode de paiement     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  8. CHANGER STATUT → PAYÉ               │
│     → Modifier le devis                 │
│     → Statut: PAYÉ                      │
│     → Mode de paiement: [choix]         │
│     → Enregistrer                       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  9. CLIENT REPART AVEC SA FACTURE       │
│     ✅ Transaction terminée              │
└─────────────────────────────────────────┘
```

---

## 💡 SCÉNARIOS D'UTILISATION

### Scénario 1: Vente Simple et Rapide

**Situation:** Client achète 3 articles

```
1. Créer devis → EN COURS
2. Ajouter 3 lignes (articles)
3. Enregistrer
4. Imprimer facture
5. Client paie en espèces
6. Changer statut → PAYÉ (Mode: Espèces)
7. Terminé! ✅
```

**Durée:** 2-3 minutes

---

### Scénario 2: Client Change d'Avis

**Situation:** Client ne veut plus acheter

```
1. Créer devis → EN COURS
2. Ajouter articles
3. Client change d'avis
4. Changer statut → ANNULÉ
   OU
   Supprimer le devis
```

---

### Scénario 3: Erreur de Saisie

**Situation:** Vous vous trompez dans les quantités

```
1. Créer devis → EN COURS
2. Ajouter articles (erreur de quantité)
3. Modifier directement les lignes
4. Corriger les quantités
5. Continuer normalement
```

---

### Scénario 4: Paiement Mobile Money

**Situation:** Client paie par M-Pesa

```
1. Créer devis → EN COURS
2. Ajouter articles
3. Enregistrer et imprimer
4. Client effectue le paiement M-Pesa
5. Vérifier réception du paiement
6. Changer statut → PAYÉ (Mode: Mobile Money)
7. Terminé! ✅
```

---

## 📋 TABLEAU DE BORD

### Statistiques Affichées

| Carte | Signification | Utilité |
|-------|---------------|---------|
| **Total Devis** | Tous les devis créés | Vue d'ensemble |
| **En cours** | Devis non finalisés | À traiter en priorité |
| **Payés** | Ventes réalisées | Chiffre d'affaires |
| **Annulés** | Ventes non abouties | Analyse des pertes |

---

## 🔒 PROTECTIONS

### Règles de Verrouillage

| Statut | Modification | Suppression | Raison |
|--------|--------------|-------------|--------|
| 🟠 **EN COURS** | ✅ Oui | ✅ Oui | Liberté totale |
| ✅ **PAYÉ** | ❌ Non 🔒 | ❌ Non 🚫 | Protection transaction |
| ❌ **ANNULÉ** | ❌ Non 🔒 | ✅ Oui | Archivage |

### Pourquoi Verrouiller les Devis Payés?

1. **Intégrité comptable** - Les transactions payées ne doivent pas changer
2. **Traçabilité** - Historique exact des ventes
3. **Conformité** - Respect des règles comptables
4. **Preuve** - Document légal en cas de litige

---

## 🎨 INDICATEURS VISUELS

### Dans la Liste

**Devis EN COURS:**
```
[👁️ Voir] [✏️ Modifier] [📄 PDF] [🗑️ Supprimer]
Badge: 🟠 Orange "En cours"
```

**Devis PAYÉ:**
```
[👁️ Voir] [🔒 Verrouillé] [📄 PDF] [🚫 Interdit]
Badge: 🟢 Vert "Payé"
```

**Devis ANNULÉ:**
```
[👁️ Voir] [🔒 Verrouillé] [📄 PDF] [🗑️ Supprimer]
Badge: 🔴 Rouge "Annulé"
```

---

## ⚡ RACCOURCIS CLAVIER (Recommandés)

Pour accélérer le travail:

- **Ctrl + N** → Nouveau devis (à configurer dans le navigateur)
- **Ctrl + P** → Imprimer la facture
- **Ctrl + S** → Enregistrer le devis

---

## 📊 RAPPORTS ET STATISTIQUES

### Informations Disponibles

1. **Nombre total de ventes** (devis payés)
2. **Ventes en cours** (devis en cours)
3. **Ventes annulées** (taux d'annulation)
4. **Chiffre d'affaires** (somme des devis payés)

### Analyse Recommandée

**Quotidienne:**
- Nombre de ventes du jour
- Chiffre d'affaires du jour
- Devis en cours non finalisés

**Hebdomadaire:**
- Total des ventes de la semaine
- Taux d'annulation
- Modes de paiement les plus utilisés

**Mensuelle:**
- Chiffre d'affaires mensuel
- Évolution par rapport au mois précédent
- Statistiques par mode de paiement

---

## 💡 CONSEILS D'UTILISATION

### ✅ Bonnes Pratiques

1. **Toujours vérifier les totaux** avant d'imprimer
2. **Changer en PAYÉ immédiatement** après paiement
3. **Sélectionner le bon mode de paiement** pour les statistiques
4. **Ne pas supprimer les devis payés** (historique important)
5. **Utiliser ANNULÉ** plutôt que supprimer (pour statistiques)

### ❌ À Éviter

1. **Ne pas laisser des devis EN COURS** indéfiniment
2. **Ne pas modifier un devis payé** (créer un nouveau si besoin)
3. **Ne pas oublier de changer le statut** après paiement
4. **Ne pas supprimer les devis payés** (protection activée)

---

## 🔧 PERSONNALISATION

### Ajouter un Mode de Paiement

Si vous utilisez un autre mode de paiement, contactez l'administrateur pour l'ajouter.

### Modifier le Taux de Main d'Œuvre

Actuellement fixé à **25%**. Pour changer ce taux, contactez l'administrateur.

---

## 📞 SUPPORT

### En Cas de Problème

1. **Devis bloqué en EN COURS** → Changer le statut ou supprimer
2. **Erreur de calcul** → Vérifier les quantités et prix unitaires
3. **Impossible de modifier** → Vérifier le statut (doit être EN COURS)
4. **Impression ne fonctionne pas** → Utiliser "Voir PDF" puis Ctrl+P

---

## 📈 ÉVOLUTIONS FUTURES

### Fonctionnalités Prévues

- 📧 Envoi automatique par email
- 📱 Application mobile
- 💰 Gestion de la caisse
- 📦 Gestion des stocks
- 👥 Base de données clients
- 📊 Graphiques de ventes
- 🧾 Génération de reçus

---

## 🎯 RÉSUMÉ RAPIDE

### Workflow en 3 Étapes

```
1. CRÉER → Ajouter articles (EN COURS)
2. IMPRIMER → Donner facture au client
3. ENCAISSER → Changer statut (PAYÉ)
```

### 3 Statuts Simples

- 🟠 **EN COURS** = En train de créer
- ✅ **PAYÉ** = Vente finalisée
- ❌ **ANNULÉ** = Vente annulée

### Protection

- **EN COURS** = Modifiable ✏️
- **PAYÉ** = Verrouillé 🔒
- **ANNULÉ** = Verrouillé 🔒

---

**Application optimisée pour la vente directe! 🛒✨**

**Bonne vente avec SHAMMAR SERVICES - MABIPINT! 💼**
