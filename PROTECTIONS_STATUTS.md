# 🔒 PROTECTIONS PAR STATUT

## SHAMMAR SERVICES - Écosystème MABIPINT

### ✅ Système de Verrouillage Implémenté

---

## 🛡️ RÈGLES DE PROTECTION

### Tableau Récapitulatif

| Statut | Modification | Suppression | Raison |
|--------|--------------|-------------|--------|
| 🟡 **BROUILLON** | ✅ Autorisée | ✅ Autorisée | Devis en cours de création |
| 🟢 **VALIDÉ** | ✅ Autorisée | ✅ Autorisée | Devis finalisé mais pas encore envoyé |
| 🔵 **ENVOYÉ** | ❌ Verrouillée | ✅ Autorisée | Devis chez le client, ne doit pas changer |
| 🟣 **ACCEPTÉ** | ❌ Verrouillée | ❌ Verrouillée | Engagement client, protection totale |
| 🔴 **REFUSÉ** | ❌ Verrouillée | ✅ Autorisée | Archivé, pas de modification |

---

## 🔐 DÉTAILS DES PROTECTIONS

### 1. 🟡 BROUILLON - Liberté Totale

**Modifications:** ✅ **AUTORISÉES**
- Vous pouvez modifier toutes les informations
- Ajouter/supprimer des lignes
- Changer le statut
- Modifier les prix

**Suppression:** ✅ **AUTORISÉE**
- Vous pouvez supprimer le devis
- Aucune restriction

**Pourquoi?**
> Le devis est en cours de création, vous devez avoir toute liberté pour le finaliser.

---

### 2. 🟢 VALIDÉ - Modifications Possibles

**Modifications:** ✅ **AUTORISÉES**
- Vous pouvez encore modifier le devis
- Utile si vous trouvez une erreur avant l'envoi
- Possibilité de revenir en brouillon

**Suppression:** ✅ **AUTORISÉE**
- Vous pouvez supprimer si nécessaire

**Pourquoi?**
> Le devis est finalisé mais pas encore envoyé au client. Vous pouvez corriger des erreurs de dernière minute.

**⚠️ Recommandation:**
- Vérifiez bien avant de passer en "ENVOYÉ"
- Une fois envoyé, les modifications seront verrouillées

---

### 3. 🔵 ENVOYÉ - Verrouillage Partiel

**Modifications:** ❌ **VERROUILLÉES**
- Le bouton "Modifier" est désactivé (icône cadenas 🔒)
- Tentative de modification → Message d'erreur
- Le devis ne peut plus être changé

**Suppression:** ✅ **AUTORISÉE**
- Vous pouvez supprimer si le devis n'est plus pertinent

**Pourquoi?**
> Le devis a été envoyé au client. Le modifier créerait une incohérence entre ce que le client a reçu et ce qui est dans le système.

**💡 Solution si modification nécessaire:**
1. Changer le statut en "BROUILLON" ou "VALIDÉ"
2. Modifier le devis
3. Remettre en "ENVOYÉ" après modification
4. Informer le client du changement

---

### 4. 🟣 ACCEPTÉ - Protection Maximale

**Modifications:** ❌ **VERROUILLÉES**
- Le bouton "Modifier" est désactivé (icône cadenas 🔒)
- Tentative de modification → Message d'erreur
- Protection totale du contenu

**Suppression:** ❌ **VERROUILLÉE**
- Le bouton "Supprimer" est désactivé (icône interdiction 🚫)
- Tentative de suppression → Message d'erreur
- Le devis est protégé

**Pourquoi?**
> Le client a accepté ce devis. C'est un engagement contractuel. Toute modification ou suppression pourrait créer des problèmes juridiques ou commerciaux.

**💡 Solution si modification nécessaire:**
1. **NE PAS modifier ce devis**
2. Créer un **nouveau devis** avec les nouvelles conditions
3. Ou créer un **avenant** (devis complémentaire)
4. Garder l'original pour l'historique

---

### 5. 🔴 REFUSÉ - Archivage

**Modifications:** ❌ **VERROUILLÉES**
- Le bouton "Modifier" est désactivé (icône cadenas 🔒)
- Le devis est archivé
- Pas de modification possible

**Suppression:** ✅ **AUTORISÉE**
- Vous pouvez supprimer si vous ne voulez pas garder l'historique
- Recommandé de garder pour les statistiques

**Pourquoi?**
> Le devis a été refusé. Il sert d'historique et de référence. Pas besoin de le modifier.

**💡 Solution si le client change d'avis:**
1. **NE PAS modifier ce devis**
2. Créer un **nouveau devis** (avec nouveau numéro)
3. Garder l'ancien pour l'historique

---

## 🎯 MESSAGES D'ERREUR

### Tentative de Modification d'un Devis Verrouillé

```
❌ Impossible de modifier un devis avec le statut "Envoyé".
   Seuls les devis en brouillon ou validés peuvent être modifiés.
```

```
❌ Impossible de modifier un devis avec le statut "Accepté".
   Seuls les devis en brouillon ou validés peuvent être modifiés.
```

```
❌ Impossible de modifier un devis avec le statut "Refusé".
   Seuls les devis en brouillon ou validés peuvent être modifiés.
```

### Tentative de Suppression d'un Devis Accepté

```
❌ Impossible de supprimer un devis accepté.
   Veuillez d'abord changer son statut.
```

---

## 🔓 COMMENT DÉBLOQUER UN DEVIS?

### Si vous devez ABSOLUMENT modifier un devis verrouillé:

#### Méthode 1: Via l'Interface (Recommandée)

1. **Aller sur le détail du devis**
2. **Changer le statut** vers "BROUILLON" ou "VALIDÉ"
   - Cela déverrouille le devis
3. **Modifier** le devis
4. **Remettre le bon statut** après modification

#### Méthode 2: Via l'Administration Django

1. **Aller sur** http://127.0.0.1:8000/admin/
2. **Cliquer sur** "Devis"
3. **Sélectionner** le devis à modifier
4. **Changer le statut** temporairement
5. **Modifier** via l'interface normale
6. **Remettre le statut** d'origine

---

## 🎨 INDICATEURS VISUELS

### Dans la Liste des Devis

**Devis Modifiable (Brouillon/Validé):**
```
[👁️ Voir] [✏️ Modifier] [📄 PDF] [🗑️ Supprimer]
```

**Devis Verrouillé (Envoyé/Refusé):**
```
[👁️ Voir] [🔒 Verrouillé] [📄 PDF] [🗑️ Supprimer]
```

**Devis Accepté (Protection Totale):**
```
[👁️ Voir] [🔒 Verrouillé] [📄 PDF] [🚫 Interdit]
```

### Dans le Détail du Devis

**Devis Modifiable:**
```
[✏️ Modifier] [📄 Voir PDF] [🖨️ Imprimer]
```

**Devis Verrouillé:**
```
[🔒 Modification verrouillée] [📄 Voir PDF] [🖨️ Imprimer]
```

---

## ⚠️ BONNES PRATIQUES

### ✅ À FAIRE:

1. **Vérifier le devis avant de l'envoyer**
   - Une fois en "ENVOYÉ", plus de modification facile

2. **Garder les devis acceptés intacts**
   - Créer un nouveau devis si besoin

3. **Utiliser les statuts correctement**
   - BROUILLON → travail en cours
   - VALIDÉ → prêt à envoyer
   - ENVOYÉ → chez le client
   - ACCEPTÉ → engagement
   - REFUSÉ → archivé

4. **Documenter les changements**
   - Si vous devez débloquer un devis, notez pourquoi

### ❌ À ÉVITER:

1. **Ne pas modifier un devis accepté**
   - Créer un nouveau devis ou un avenant

2. **Ne pas supprimer les devis acceptés**
   - Ils servent de preuve et d'historique

3. **Ne pas changer le statut sans raison**
   - Chaque statut a un sens

4. **Ne pas envoyer un brouillon**
   - Toujours passer par "VALIDÉ" d'abord

---

## 🔄 WORKFLOW AVEC PROTECTIONS

### Scénario Normal

```
1. Créer devis → BROUILLON ✏️
   ↓ (modifications libres)
2. Finaliser → VALIDÉ ✅
   ↓ (dernières vérifications possibles)
3. Envoyer → ENVOYÉ 🔒
   ↓ (verrouillé, attente réponse)
4. Réponse client → ACCEPTÉ 🔒🔒 ou REFUSÉ 🔒
```

### Scénario avec Correction Nécessaire

```
1. Devis en ENVOYÉ 🔒
   ↓
2. Erreur détectée!
   ↓
3. Changer statut → BROUILLON ✏️
   ↓
4. Corriger le devis
   ↓
5. Valider → VALIDÉ ✅
   ↓
6. Renvoyer → ENVOYÉ 🔒
   ↓
7. Informer le client du changement
```

---

## 📊 RÉSUMÉ VISUEL

```
┌─────────────────────────────────────────────────────────┐
│                  NIVEAU DE PROTECTION                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  BROUILLON    [░░░░░░░░░░] 0%  - Aucune protection     │
│  VALIDÉ       [░░░░░░░░░░] 0%  - Aucune protection     │
│  ENVOYÉ       [████████░░] 80% - Modification bloquée   │
│  ACCEPTÉ      [██████████] 100% - Protection totale     │
│  REFUSÉ       [████████░░] 80% - Modification bloquée   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎓 FORMATION UTILISATEURS

### Points Clés à Retenir:

1. **Brouillon et Validé** = Liberté totale ✅
2. **Envoyé et Refusé** = Modification verrouillée 🔒
3. **Accepté** = Protection maximale 🔒🔒
4. **Toujours vérifier avant d'envoyer** ⚠️
5. **Créer un nouveau devis plutôt que modifier un accepté** 💡

---

## 🆘 FAQ

**Q: J'ai envoyé un devis avec une erreur, que faire?**
> R: Changez le statut en "BROUILLON", corrigez, revalidez, et renvoyez. Informez le client.

**Q: Le client a accepté mais veut changer quelque chose?**
> R: Créez un NOUVEAU devis avec les modifications. Gardez l'ancien pour l'historique.

**Q: Pourquoi je ne peux pas supprimer un devis accepté?**
> R: C'est un engagement contractuel. Il doit rester dans le système pour l'historique et la comptabilité.

**Q: Comment voir tous les devis verrouillés?**
> R: Dans la liste, cherchez les icônes de cadenas 🔒 au lieu des icônes de modification ✏️.

**Q: Puis-je changer le statut d'un devis accepté?**
> R: Oui, via l'interface admin, mais ce n'est pas recommandé sauf cas exceptionnel.

---

**Système de protection activé! Vos devis sont maintenant sécurisés! 🔒✨**
