# 🚀 Guide de Démarrage Rapide - Amazon Scraper Pro

## Installation en 3 étapes

### 1️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2️⃣ Lancer l'application
```bash
streamlit run app.py
```
Ou simplement :
```bash
./start.sh
```

### 3️⃣ Ouvrir dans le navigateur
L'application s'ouvre automatiquement à : **http://localhost:8501**

---

## 📋 Utilisation

### 🔍 Faire un Scraping

1. Menu : **🔍 Scraping**
2. Remplir :
   - Mot-clé : `"laptop"` 
   - Nombre : `100`
   - Pages : `20`
3. Cliquer : **🚀 Lancer le scraping**
4. Attendre la fin (barre de progression)
5. Télécharger CSV ou Excel

### 📊 Consolider et Analyser

1. Menu : **📊 Consolidation & Analyse**
2. Cliquer : **🔄 Consolider tous les fichiers**
3. Télécharger le fichier consolidé
4. Consulter les analyses :
   - Statistiques (prix moyen, min, max)
   - Graphiques de distribution
   - Top 10 produits

### 📁 Gérer les Fichiers

1. Menu : **📁 Fichiers**
2. Naviguer dans les onglets :
   - **CSV** : Fichiers individuels
   - **Excel** : Fichiers individuels
   - **Consolidés** : Fichiers regroupés
3. Télécharger les fichiers souhaités

---

## 📊 Résultats

### Fichiers générés

#### Scraping individuel
- `amazon_Thriller_20240207_143022.csv`
- `amazon_Thriller_20240207_143022.xlsx`

#### Consolidation
- `bd_scraping_amazone_20240207.csv`
- `bd_scraping_amazone_20240207.xlsx`

### Colonnes des données
| Colonne | Description |
|---------|-------------|
| ASIN | Identifiant unique Amazon |
| Titre | Nom du produit |
| Prix | Prix avec devise |
| Note | Note sur 5 étoiles |
| Nb_Avis | Nombre d'avis |

---

## 📈 Analyses Disponibles

### Statistiques Clés
- 📦 Total de produits
- 💰 Prix moyen
- 💵 Prix minimum
- 💎 Prix maximum

### Visualisations
- 📊 Distribution des prix (histogramme)
- ⭐ Distribution des notes (histogramme)
- 📦 Box plot des prix

### Top 10
- 💎 Produits les plus chers
- 💵 Produits les moins chers
- ❤️ Produits les plus aimés (note × avis)

---

## 💡 Conseils

### Test Rapide
```
Mot-clé : "laptop"
Produits : 50
Pages : 5
Durée : ~2-3 minutes
```

### Recherche Complète
```
Mot-clé : "business books"
Produits : 500
Pages : 100
Durée : ~15-20 minutes
```

### Mots-clés Populaires
- 📚 Livres : `"Thriller"`, `"Science Fiction"`
- 💻 Tech : `"laptop"`, `"headphones"`
- 🏠 Maison : `"kitchen tools"`, `"furniture"`

---

## ⚠️ Dépannage

### Problème : Connexion échouée
**Solution** : 
- Vérifier la connexion internet
- Attendre quelques minutes
- Relancer le scraping

### Problème : Pas de prix
**Solution** :
- Normal pour certains produits
- Supprimés automatiquement lors de la consolidation

### Problème : Application ne démarre pas
**Solution** :
```bash
pip install --upgrade streamlit
streamlit run app.py
```

---

## 📞 Support

Pour plus d'informations, consulter le **README.md** complet.

---

**Version** : 1.0.0
**Durée moyenne** : 2-3 min pour 100 produits
