# 🚀 Guide de Déploiement - Streamlit Community Cloud

## 📋 Prérequis

1. Compte GitHub : https://github.com/signup
2. Compte Streamlit Cloud : https://share.streamlit.io

---

## 🎯 Méthode 1 : Via Interface GitHub (PLUS FACILE)

### Étape 1 : Créer un dépôt GitHub

1. Allez sur https://github.com/new
2. Remplissez :
   - **Repository name** : `amazon-scraper-pro`
   - **Description** : Application de scraping Amazon avec analyses
   - **Public** ou **Private** (au choix)
3. ✅ Cochez "Add a README file"
4. Cliquez **"Create repository"**

### Étape 2 : Uploader les fichiers

1. Dans votre nouveau dépôt, cliquez **"Add file"** → **"Upload files"**

2. Glissez-déposez TOUS ces fichiers :
   ```
   ✓ app.py
   ✓ requirements.txt
   ✓ packages.txt
   ✓ README.md
   ✓ QUICKSTART.md
   ✓ config.py
   ✓ generate_demo_data.py
   ```

3. Dans la zone "Commit changes" en bas :
   - Message : `Initial commit - Amazon Scraper Pro`
   - Cliquez **"Commit changes"**

4. ✅ Attendez que les fichiers soient uploadés

### Étape 3 : Déployer sur Streamlit Cloud

1. Allez sur https://share.streamlit.io

2. Cliquez **"Sign in with GitHub"**

3. Autorisez Streamlit à accéder à votre GitHub

4. Cliquez **"New app"**

5. Remplissez :
   - **Repository** : Sélectionnez `votre-username/amazon-scraper-pro`
   - **Branch** : `main` (par défaut)
   - **Main file path** : `app.py`

6. **Advanced settings** (optionnel) :
   - Python version : `3.10`

7. Cliquez **"Deploy!"**

8. ⏳ Attendez 2-5 minutes (première installation)

9. 🎉 Votre app sera disponible à : `https://votre-app-name.streamlit.app`

---

## 🎯 Méthode 2 : Via Git et Terminal (POUR DÉVELOPPEURS)

### Étape 1 : Installer Git

**Windows** : https://git-scm.com/download/win
**Mac** : `brew install git`
**Linux** : `sudo apt-get install git`

### Étape 2 : Configurer Git (première fois)

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

### Étape 3 : Créer le dépôt local

```bash
# 1. Créer un dossier pour votre projet
mkdir amazon-scraper-pro
cd amazon-scraper-pro

# 2. Copier tous les fichiers téléchargés dans ce dossier

# 3. Initialiser Git
git init

# 4. Ajouter tous les fichiers
git add .

# 5. Premier commit
git commit -m "Initial commit - Amazon Scraper Pro"
```

### Étape 4 : Créer le dépôt GitHub

1. Allez sur https://github.com/new
2. Nom : `amazon-scraper-pro`
3. **NE COCHEZ PAS** "Add a README file"
4. Cliquez "Create repository"
5. Copiez l'URL qui apparaît (ex: `https://github.com/username/amazon-scraper-pro.git`)

### Étape 5 : Pousser le code

```bash
# Remplacez USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/USERNAME/amazon-scraper-pro.git
git branch -M main
git push -u origin main
```

### Étape 6 : Déployer sur Streamlit Cloud

Suivez l'Étape 3 de la Méthode 1 ci-dessus.

---

## 🎯 Méthode 3 : Exécution Locale (SANS DÉPLOIEMENT)

Si vous voulez juste tester localement :

### Installation

```bash
# 1. Télécharger tous les fichiers dans un dossier

# 2. Ouvrir un terminal dans ce dossier

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py
```

### Utilisation

- L'application s'ouvre automatiquement dans votre navigateur
- URL : `http://localhost:8501`
- Pour arrêter : `Ctrl+C` dans le terminal

---

## ⚠️ Notes Importantes

### Fichiers Requis pour Streamlit Cloud

Pour que l'application fonctionne sur Streamlit Cloud, vous DEVEZ avoir :

1. **app.py** - Application principale
2. **requirements.txt** - Dépendances Python
3. **packages.txt** - Dépendances système (Chrome)

### Limitations de Streamlit Cloud

- **Resources limitées** : Scraping peut être lent
- **Timeout** : Maximum 10 minutes par requête
- **Stockage temporaire** : Fichiers supprimés après redémarrage
- **CAPTCHA** : Peut être bloqué par Amazon

### Recommandations

Pour une utilisation optimale :

1. **Développement et tests** : Exécution locale
2. **Démonstration** : Streamlit Cloud avec données de test
3. **Production** : Serveur dédié (AWS, DigitalOcean, etc.)

---

## 🐛 Dépannage

### Erreur : "chromium not found"

**Solution** : Vérifiez que `packages.txt` est bien présent avec :
```
chromium
chromium-driver
```

### Erreur : "ModuleNotFoundError"

**Solution** : Vérifiez que `requirements.txt` contient toutes les dépendances :
```
streamlit==1.31.0
pandas==2.1.4
selenium==4.16.0
webdriver-manager==4.0.1
openpyxl==3.1.2
plotly==5.18.0
```

### Erreur : "Could not reach host"

**Solution** :
- Amazon bloque parfois Streamlit Cloud
- Testez en local
- Utilisez les données de démonstration : `python generate_demo_data.py`

### App ne démarre pas

**Solution** :
1. Vérifiez les logs dans Streamlit Cloud
2. Cliquez sur "⋮" → "View logs"
3. Cherchez les erreurs
4. Redéployez : "⋮" → "Reboot app"

---

## 📊 Structure Finale du Dépôt GitHub

```
amazon-scraper-pro/
├── app.py                      # Application principale
├── requirements.txt            # Dépendances Python
├── packages.txt               # Dépendances système
├── config.py                  # Configuration
├── generate_demo_data.py      # Générateur de données de test
├── README.md                  # Documentation complète
├── QUICKSTART.md             # Guide rapide
└── DEPLOYMENT.md             # Ce fichier
```

---

## ✅ Checklist de Déploiement

- [ ] Compte GitHub créé
- [ ] Dépôt GitHub créé
- [ ] Fichiers uploadés sur GitHub
- [ ] Compte Streamlit Cloud créé
- [ ] App déployée sur Streamlit Cloud
- [ ] App testée et fonctionnelle

---

## 🎉 Après le Déploiement

Votre application sera accessible à :
```
https://votre-app-name.streamlit.app
```

Vous pouvez :
- ✅ Partager le lien avec d'autres
- ✅ Modifier le code et redéployer automatiquement
- ✅ Consulter les logs et métriques
- ✅ Configurer un domaine personnalisé (plan payant)

---

## 📞 Besoin d'Aide ?

- Documentation Streamlit : https://docs.streamlit.io/streamlit-community-cloud
- GitHub Guides : https://guides.github.com
- Support Streamlit : https://discuss.streamlit.io

---

**Bonne chance avec votre déploiement !** 🚀
