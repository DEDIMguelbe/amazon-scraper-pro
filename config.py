# Configuration de l'Application Amazon Scraper Pro

## Paramètres de Scraping

### Délais anti-détection (en secondes)
HUMAN_DELAY_MIN = 3.0
HUMAN_DELAY_MAX = 7.0
TYPING_DELAY_MIN = 0.1
TYPING_DELAY_MAX = 0.3

### Mode navigateur
HEADLESS_MODE = True  # False pour voir le navigateur

### User Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0"

## Paramètres d'Export

### Format de date pour les fichiers
DATE_FORMAT = "%Y%m%d"
DATETIME_FORMAT = "%Y%m%d_%H%M%S"

### Nom des fichiers consolidés
CONSOLIDATED_PREFIX = "bd_scraping_amazone"

## Paramètres d'Interface

### Couleurs
PRIMARY_COLOR = "#FF9900"  # Orange Amazon
SECONDARY_COLOR = "#232F3E"  # Bleu foncé Amazon

### Limites
MAX_PRODUCTS = 1000
MAX_PAGES = 100
MIN_PRODUCTS = 10
MIN_PAGES = 1

## Paramètres d'Analyse

### Nombre de produits dans les tops
TOP_N_PRODUCTS = 10

### Bins pour histogrammes
PRICE_BINS = 50
RATING_BINS = 20
