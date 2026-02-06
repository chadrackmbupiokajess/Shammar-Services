# 🚀 GUIDE D'INSTALLATION RAPIDE

## SHAMMAR SERVICES - Écosystème MABIPINT

### ⚡ Installation en 7 étapes

#### 1️⃣ Créer l'environnement virtuel

```powershell
python -m venv venv
```

#### 2️⃣ Activer l'environnement virtuel

```powershell
.\venv\Scripts\Activate
```

Vous devriez voir `(venv)` apparaître dans votre terminal.

#### 3️⃣ Installer Django et les dépendances

```powershell
pip install -r requirements.txt
```

#### 4️⃣ Créer les migrations de la base de données

```powershell
python manage.py makemigrations
```

#### 5️⃣ Appliquer les migrations

```powershell
python manage.py migrate
```

#### 6️⃣ Créer un compte administrateur

```powershell
python manage.py createsuperuser
```

Remplissez les informations demandées:
- **Nom d'utilisateur**: (votre choix, ex: admin)
- **Email**: (optionnel)
- **Mot de passe**: (choisissez un mot de passe sécurisé)
- **Confirmation du mot de passe**: (répétez le mot de passe)

#### 7️⃣ Lancer le serveur

```powershell
python manage.py runserver
```

### ✅ Accéder à l'application

Une fois le serveur lancé, ouvrez votre navigateur et accédez à:

- **Application principale**: http://127.0.0.1:8000/
- **Interface d'administration**: http://127.0.0.1:8000/admin/

### 🔐 Première connexion

1. Allez sur http://127.0.0.1:8000/
2. Connectez-vous avec le compte créé à l'étape 6
3. Vous arriverez sur le tableau de bord

### 📝 Créer votre premier devis

1. Cliquez sur **"Nouveau Devis"**
2. Remplissez les informations du client
3. Cliquez sur **"Ajouter une ligne"** pour ajouter des produits/services
4. Les totaux se calculent automatiquement
5. Cliquez sur **"Enregistrer le devis"**

### 🎨 Fonctionnalités disponibles

- ✅ Créer des devis
- ✅ Modifier des devis
- ✅ Voir les détails
- ✅ Exporter en PDF (avec filigrane)
- ✅ Imprimer les devis
- ✅ Gérer les statuts (brouillon, validé, accepté, etc.)
- ✅ Calculs automatiques (Total Fourniture, M.O 25%, Total Général)

### 🛠️ Commandes utiles

#### Arrêter le serveur
Appuyez sur `Ctrl + C` dans le terminal

#### Relancer le serveur
```powershell
python manage.py runserver
```

#### Créer un nouveau super utilisateur
```powershell
python manage.py createsuperuser
```

#### Réinitialiser la base de données (⚠️ ATTENTION: supprime toutes les données)
```powershell
Remove-Item db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### 📊 Structure de l'application

```
D:/Shammar Services/
├── shammar_services/      # Configuration Django
├── mabipint/             # Application principale
│   ├── models.py         # Modèles de données
│   ├── views.py          # Logique métier
│   ├── forms.py          # Formulaires
│   ├── urls.py           # Routes
│   ├── admin.py          # Interface admin
│   └── templates/        # Templates HTML
├── static/               # Fichiers statiques
├── media/                # Fichiers uploadés
├── manage.py             # Script de gestion Django
├── requirements.txt      # Dépendances Python
└── db.sqlite3           # Base de données (créée après migration)
```

### ❓ Problèmes courants

#### "Django n'est pas reconnu"
Assurez-vous que l'environnement virtuel est activé (`.\venv\Scripts\Activate`)

#### "No module named 'django'"
Installez les dépendances: `pip install -r requirements.txt`

#### "Table doesn't exist"
Exécutez les migrations: `python manage.py migrate`

#### Mot de passe oublié
Créez un nouveau super utilisateur: `python manage.py createsuperuser`

### 🎯 Prochaines étapes

1. ✅ Créer votre premier devis
2. ✅ Explorer l'interface d'administration
3. ✅ Personnaliser les informations de l'entreprise
4. ✅ Ajouter un logo (optionnel)

### 📞 Support

Pour toute question, contactez l'administrateur système.

---

**Bon travail avec SHAMMAR SERVICES - MABIPINT! 🚀**
