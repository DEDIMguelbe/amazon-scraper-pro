"""
Script de génération de données de démonstration
Pour tester l'application sans faire de scraping réel
"""

import pandas as pd
import random
from datetime import datetime
from pathlib import Path

# Configuration
Config_OUTPUT_DIR = Path("amazon_results")
Config_CSV_DIR = Config_OUTPUT_DIR / "csv"
Config_EXCEL_DIR = Config_OUTPUT_DIR / "excel"

# Créer les dossiers
for d in [Config_CSV_DIR, Config_EXCEL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Données de démonstration
categories = ["Thriller", "Science Fiction", "Romance", "Business Books", "Tech"]
titles = [
    "The Silent Patient", "Where the Crawdads Sing", "Project Hail Mary",
    "The Midnight Library", "Atomic Habits", "Dune", "1984", "Sapiens",
    "The Psychology of Money", "Thinking, Fast and Slow", "The Alchemist",
    "Deep Work", "Can't Hurt Me", "Educated", "Becoming", "The Power of Now",
    "Steve Jobs Biography", "The Lean Startup", "Good to Great", "Zero to One"
]

def generate_demo_data(category, num_products=100):
    """Génère des données de démonstration pour une catégorie"""
    data = []
    
    for i in range(num_products):
        # ASIN aléatoire
        asin = f"B0{random.randint(10000000, 99999999):08d}"
        
        # Titre aléatoire
        title = random.choice(titles) + f" - Edition {random.choice(['Deluxe', 'Premium', 'Standard', 'Collector'])}"
        
        # Prix aléatoire
        price = round(random.uniform(5.99, 99.99), 2)
        price_str = f"$ {price}"
        
        # Note aléatoire
        rating = round(random.uniform(3.0, 5.0), 1)
        
        # Nombre d'avis aléatoire
        reviews = random.randint(10, 50000)
        
        data.append({
            "ASIN": asin,
            "Titre": title,
            "Prix": price_str,
            "Note": str(rating),
            "Nb_Avis": str(reviews)
        })
    
    return data

def create_demo_files():
    """Crée des fichiers de démonstration pour chaque catégorie"""
    print("🎨 Génération de données de démonstration...")
    
    for category in categories:
        num_products = random.randint(80, 150)
        data = generate_demo_data(category, num_products)
        
        # DataFrame
        df = pd.DataFrame(data)
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"amazon_{category.replace(' ', '_')}_{timestamp}"
        
        # CSV
        csv_path = Config_CSV_DIR / f"{filename_base}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ CSV créé : {csv_path.name}")
        
        # Excel
        excel_path = Config_EXCEL_DIR / f"{filename_base}.xlsx"
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"✅ Excel créé : {excel_path.name}")
    
    print(f"\n🎉 {len(categories)} fichiers de démonstration créés !")
    print(f"📁 Dossier : {Config_OUTPUT_DIR.resolve()}")
    print("\n💡 Vous pouvez maintenant tester la consolidation et l'analyse dans Streamlit")

if __name__ == "__main__":
    create_demo_files()
