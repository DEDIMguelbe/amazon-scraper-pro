# 🛒 Amazon Scraper Pro - Application Streamlit

Application complète de scraping Amazon avec consolidation, analyse et export des données.

## ✨ Fonctionnalités

### 🔍 Scraping Automatique
- Extraction automatique des produits Amazon
- Paramètres personnalisables (mot-clé, nombre de produits, pages)
- Barre de progression en temps réel
- Export instantané CSV et Excel

### 📊 Consolidation & Analyse
- **Consolidation automatique** : Combine tous les fichiers scrapés en un seul
- **Nettoyage des données** : Suppression des produits sans prix et des doublons
- **Analyses descriptives** :
  - Statistiques des prix (moyenne, médiane, min, max)
  - Top 10 produits les plus chers
  - Top 10 produits les moins chers
  - Top 10 produits les plus aimés (note × nombre d'avis)
- **Visualisations** :
  - Distribution des prix (histogramme)
  - Distribution des notes (histogramme)
  - Box plot des prix
  - Graphiques interactifs avec Plotly

### 📥 Export & Téléchargement
- Fichiers consolidés nommés : `bd_scraping_amazone_AAAAMMJJ`
- Format CSV et Excel disponibles
- Interface de téléchargement intuitive
- Gestion centralisée des fichiers

### 🎨 Interface Moderne
- Design inspiré d'Amazon (orange #FF9900)
- Layout responsive en 3 pages
- Animations et feedbacks visuels

## 📦 Installation

### 1. Cloner ou télécharger le projet

```bash
git clone <votre-repo>
cd amazon-scraper-pro
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Installer Chrome/Chromium

L'application utilise Selenium avec Chrome. Assurez-vous d'avoir Chrome ou Chromium installé :

**Ubuntu/Debian :**
```bash
sudo apt-get update
sudo apt-get install chromium-browser chromium-chromedriver
```

**Windows/Mac :**
Téléchargez Chrome depuis https://www.google.com/chrome/

## 🚀 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

### Navigation

#### 📋 Menu : 🔍 Scraping
1. Entrez le **mot-clé** de recherche (ex: "Thriller", "laptop", "headphones")
2. Définissez le **nombre de produits** à scraper (10-1000)
3. Choisissez le **nombre de pages** maximum (1-100)
4. Cliquez sur **🚀 Lancer le scraping**
5. Attendez la fin du scraping (barre de progression)
6. Téléchargez les résultats en CSV ou Excel

#### 📋 Menu : 📊 Consolidation & Analyse
1. Cliquez sur **🔄 Consolider tous les fichiers**
2. Le système :
   - Lit tous les fichiers CSV existants
   - Supprime les produits sans prix
   - Supprime les doublons (par ASIN)
   - Crée le fichier consolidé `bd_scraping_amazone_AAAAMMJJ`
3. Téléchargez le fichier consolidé (CSV ou Excel)
4. Consultez l'**analyse descriptive** :
   - Métriques clés (total, prix moyen, min, max)
   - Graphiques de distribution
   - Top 10 des produits (chers, moins chers, aimés)

#### 📋 Menu : 📁 Fichiers
- **CSV** : Liste de tous les fichiers CSV avec téléchargement
- **Excel** : Liste de tous les fichiers Excel avec téléchargement
- **Consolidés** : Fichiers consolidés disponibles

## 📂 Structure des Dossiers

```
amazon_results/
├── csv/                    # Fichiers CSV individuels
│   └── amazon_Thriller_20240207_143022.csv
├── excel/                  # Fichiers Excel individuels
│   └── amazon_Thriller_20240207_143022.xlsx
├── consolidated/           # Fichiers consolidés
│   ├── bd_scraping_amazone_20240207.csv
│   └── bd_scraping_amazone_20240207.xlsx
└── debug/                  # Logs de débogage
```

## 📊 Format des Données

### Colonnes extraites :
- **ASIN** : Identifiant unique Amazon
- **Titre** : Nom du produit
- **Prix** : Prix avec devise
- **Note** : Note sur 5 étoiles
- **Nb_Avis** : Nombre d'avis clients

### Exemple :
```csv
ASIN,Titre,Prix,Note,Nb_Avis
B08N5WRWNW,The Silent Patient,$ 14.99,4.5,12847
B07XJ8C8F7,Where the Crawdads Sing,$ 16.80,4.7,28934
...
```

## ⚙️ Configuration Avancée

### Modifier les délais anti-détection

Dans `app.py`, ajustez la classe `Config` :

```python
class Config:
    HUMAN_MIN, HUMAN_MAX = 3.0, 7.0      # Délai entre actions (secondes)
    TYPING_MIN, TYPING_MAX = 0.1, 0.3    # Délai entre caractères
```

### Mode headless (sans interface)

Par défaut, Chrome tourne en mode headless. Pour voir le navigateur :

```python
def creer_driver():
    options = Options()
    # options.add_argument("--headless")  # Commenter cette ligne
    ...
```

## 🐛 Dépannage

### Erreur "Could not reach host"
- Vérifiez votre connexion internet
- Amazon peut bloquer après trop de requêtes
- Attendez quelques minutes et réessayez
- Utilisez un VPN si nécessaire

### CAPTCHA détecté
- L'application détecte les CAPTCHAs
- En mode non-headless, résolvez-le manuellement
- L'application attendra 60 secondes

### Fichiers non trouvés
- Vérifiez que le dossier `amazon_results/` existe
- Lancez au moins un scraping avant de consolider

### Produits sans prix
- Certains produits n'affichent pas de prix publiquement
- Ils sont automatiquement supprimés lors de la consolidation

## 🎯 Conseils d'Utilisation

### Pour des tests rapides
```
Mot-clé : "laptop"
Nombre : 50
Pages : 5
```

### Pour une recherche complète
```
Mot-clé : "business books"
Nombre : 500
Pages : 100
```

### Mots-clés populaires
- Romans : "Thriller", "Science Fiction", "Romance"
- Tech : "laptop", "headphones", "smartphone"
- Livres : "business books", "cooking books"

## 📈 Analyses Disponibles

### Statistiques
- Total de produits uniques
- Prix moyen
- Prix médian
- Prix minimum
- Prix maximum

### Classements Top 10
1. **Plus Chers** : Produits avec les prix les plus élevés
2. **Moins Chers** : Produits avec les prix les plus bas
3. **Plus Aimés** : Basé sur Score = Note × Nb_Avis

### Visualisations
- **Histogramme des prix** : Distribution des prix
- **Histogramme des notes** : Distribution des évaluations
- **Box Plot** : Analyse statistique des prix (quartiles, outliers)

## 🔒 Respect des Conditions d'Utilisation

⚠️ **Important** :
- Cette application est destinée à un usage éducatif et de recherche
- Respectez les conditions d'utilisation d'Amazon
- N'abusez pas du scraping (rate limiting)
- Utilisez les délais aléatoires pour simuler un comportement humain

## 🛠️ Technologies Utilisées

- **Streamlit** : Interface web interactive
- **Selenium** : Automation du navigateur
- **Pandas** : Manipulation et analyse de données
- **Plotly** : Visualisations interactives
- **openpyxl** : Génération de fichiers Excel

## 📝 Licence

MIT License - Utilisation libre pour usage personnel et éducatif

---

**Version** : 1.0.0  
**Date** : Février 2024
