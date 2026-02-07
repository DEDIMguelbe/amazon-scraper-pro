import streamlit as st
import pandas as pd
import time
import random
import re
from datetime import datetime
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import io
import base64

# Configuration de la page
st.set_page_config(
    page_title="Amazon Scraper Pro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec SweetAlert
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF9900;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #232F3E 0%, #37475A 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF9900;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #E68A00;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>

<!-- SweetAlert2 -->
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
""", unsafe_allow_html=True)


# Classe de configuration
class Config:
    OUTPUT_DIR = Path("amazon_results")
    CSV_DIR = OUTPUT_DIR / "csv"
    EXCEL_DIR = OUTPUT_DIR / "excel"
    DEBUG_DIR = OUTPUT_DIR / "debug"
    CONSOLIDATED_DIR = OUTPUT_DIR / "consolidated"
    HUMAN_MIN, HUMAN_MAX = 3.0, 7.0
    TYPING_MIN, TYPING_MAX = 0.1, 0.3
    
    @classmethod
    def setup(cls):
        for d in [cls.CSV_DIR, cls.EXCEL_DIR, cls.DEBUG_DIR, cls.CONSOLIDATED_DIR]:
            d.mkdir(parents=True, exist_ok=True)


# Fonctions de scraping
def creer_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0"
    options.add_argument(f"user-agent={ua}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def sleep_humain(min_s=None, max_s=None):
    time.sleep(random.uniform(min_s or Config.HUMAN_MIN, max_s or Config.HUMAN_MAX))


def taper_humain(element, texte):
    element.clear()
    time.sleep(0.3)
    for char in texte:
        element.send_keys(char)
        time.sleep(random.uniform(Config.TYPING_MIN, Config.TYPING_MAX))


def scroll_humain(driver):
    hauteur = driver.execute_script("return document.body.scrollHeight")
    pos = 0
    while pos < hauteur:
        pos += random.randint(200, 400)
        driver.execute_script(f"window.scrollTo(0, {pos});")
        time.sleep(random.uniform(0.3, 0.8))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7);")
    time.sleep(0.5)


def connecter_amazon(driver):
    driver.get("https://www.amazon.com")
    sleep_humain(3, 5)
    if "captcha" in driver.page_source.lower():
        return False
    scroll_humain(driver)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "nav-logo")))
        return True
    except:
        return False


def rechercher(driver, mot_cle):
    barre = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
    barre.click()
    sleep_humain(0.5, 1.0)
    taper_humain(barre, mot_cle)
    sleep_humain(0.5, 1.0)
    barre.send_keys(Keys.RETURN)
    sleep_humain(4, 6)
    scroll_humain(driver)
    for sel in ["div[data-component-type='s-search-result']", "div.s-result-item[data-asin]"]:
        if len(driver.find_elements(By.CSS_SELECTOR, sel)) > 0:
            return True
    return False


def extraire_prix_ultime(elem):
    """7 stratégies pour extraire le prix"""
    
    # Stratégie 1: a-offscreen
    try:
        prix = elem.find_element(By.CSS_SELECTOR, "span.a-price span.a-offscreen").text.strip()
        if prix and len(prix) > 1:
            return ' '.join(prix.split())
    except:
        pass
    
    # Stratégie 2: Symbole + Whole + Fraction
    try:
        symbol = ""
        try:
            symbol = elem.find_element(By.CSS_SELECTOR, "span.a-price-symbol").text.strip()
        except:
            pass
        whole = elem.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip()
        if whole:
            try:
                fraction = elem.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text.strip()
                return f"{symbol} {whole}.{fraction}".strip()
            except:
                return f"{symbol} {whole}".strip()
    except:
        pass
    
    # Stratégie 3: Texte conteneur
    try:
        prix_container = elem.find_element(By.CSS_SELECTOR, "span.a-price")
        prix_text = prix_container.text.strip()
        if prix_text:
            prix = prix_text.split('\n')[0].strip()
            if len(prix) > 1:
                return prix
    except:
        pass
    
    # Stratégie 4: Regex
    try:
        html = elem.get_attribute('innerHTML')
        patterns = [
            r'[\$€£¥XAF]\s*[\d,]+\.?\d*',
            r'[\d,]+\.?\d*\s*[\$€£¥]',
            r'FCFA\s*[\d\s,]+',
            r'[\d\s,]+\s*FCFA'
        ]
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(0).strip()
    except:
        pass
    
    return None


def extraire_note(elem):
    try:
        note_elem = elem.find_element(By.CSS_SELECTOR, "span.a-icon-alt")
        note_text = note_elem.get_attribute("textContent") or note_elem.text
        match = re.search(r'([\d.]+)\s*(?:out of|sur|de)\s*5', note_text)
        if match:
            return match.group(1)
    except:
        pass
    return None


def extraire_avis(elem):
    try:
        avis = elem.find_element(By.CSS_SELECTOR, "span.s-underline-text").text.strip()
        avis = re.sub(r'[^\d]', '', avis)
        return avis if avis else None
    except:
        return None


def extraire_produits_page(driver):
    produits = []
    selectors = [
        "div[data-component-type='s-search-result']",
        "div.s-result-item[data-asin]",
        "div[data-asin]:not([data-asin=''])"
    ]
    
    elements = []
    for sel in selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, sel)
        if elements:
            break
    
    for elem in elements:
        try:
            asin = elem.get_attribute("data-asin")
            if not asin or len(asin) < 10:
                continue
                
            titre_elem = elem.find_elements(By.CSS_SELECTOR, "h2 a span, h2 span")
            titre = titre_elem[0].text.strip() if titre_elem else None
            
            if not titre or len(titre) < 3:
                continue
            
            prix = extraire_prix_ultime(elem)
            note = extraire_note(elem)
            avis = extraire_avis(elem)
            
            produits.append({
                "ASIN": asin,
                "Titre": titre,
                "Prix": prix,
                "Note": note,
                "Nb_Avis": avis
            })
        except:
            continue
    
    return produits


def scraper(mot_cle, nb_produits, max_pages, progress_bar, status_text):
    Config.setup()
    driver = None
    donnees = []
    
    try:
        status_text.text("🔧 Initialisation du driver...")
        driver = creer_driver()
        
        status_text.text("🌐 Connexion à Amazon...")
        if not connecter_amazon(driver):
            status_text.error("❌ Échec de connexion à Amazon")
            return None
        
        status_text.text(f"🔍 Recherche: {mot_cle}")
        if not rechercher(driver, mot_cle):
            status_text.error("❌ Échec de la recherche")
            return None
        
        page = 1
        while len(donnees) < nb_produits and page <= max_pages:
            status_text.text(f"📄 Page {page}/{max_pages} - Produits: {len(donnees)}/{nb_produits}")
            
            produits_page = extraire_produits_page(driver)
            donnees.extend(produits_page)
            
            progress = min(len(donnees) / nb_produits, 1.0)
            progress_bar.progress(progress)
            
            if len(donnees) >= nb_produits:
                break
            
            # Page suivante
            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
                if "s-pagination-disabled" in next_btn.get_attribute("class"):
                    break
                next_btn.click()
                sleep_humain(4, 6)
                scroll_humain(driver)
            except:
                break
            
            page += 1
        
        return donnees[:nb_produits]
        
    except Exception as e:
        status_text.error(f"❌ Erreur: {e}")
        return None
    finally:
        if driver:
            driver.quit()


def exporter_scraping(donnees, mot_cle):
    """Exporte les données scrapées"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"amazon_{mot_cle.replace(' ', '_')}_{timestamp}"
    
    df = pd.DataFrame(donnees)
    
    # CSV
    csv_path = Config.CSV_DIR / f"{filename_base}.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    # Excel
    excel_path = Config.EXCEL_DIR / f"{filename_base}.xlsx"
    df.to_excel(excel_path, index=False, engine='openpyxl')
    
    return csv_path, excel_path


def consolider_fichiers():
    """Consolide tous les fichiers CSV et Excel en un seul"""
    all_data = []
    
    # Lire tous les CSV
    for csv_file in Config.CSV_DIR.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)
            all_data.append(df)
        except:
            continue
    
    if not all_data:
        return None, None
    
    # Concaténer
    df_consolidated = pd.concat(all_data, ignore_index=True)
    
    # Supprimer les produits sans prix
    df_consolidated = df_consolidated[df_consolidated['Prix'].notna()]
    df_consolidated = df_consolidated[df_consolidated['Prix'] != '']
    
    # Supprimer les doublons
    df_consolidated = df_consolidated.drop_duplicates(subset=['ASIN'], keep='first')
    
    # Nom du fichier avec date
    date_str = datetime.now().strftime("%Y%m%d")
    filename_base = f"bd_scraping_amazone_{date_str}"
    
    # Sauvegarder CSV
    csv_path = Config.CONSOLIDATED_DIR / f"{filename_base}.csv"
    df_consolidated.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    # Sauvegarder Excel
    excel_path = Config.CONSOLIDATED_DIR / f"{filename_base}.xlsx"
    df_consolidated.to_excel(excel_path, index=False, engine='openpyxl')
    
    return csv_path, excel_path, df_consolidated


def analyser_donnees(df):
    """Analyse descriptive des données"""
    analyses = {}
    
    # Nettoyer et convertir les prix
    def nettoyer_prix(prix_str):
        if pd.isna(prix_str):
            return None
        prix_str = str(prix_str)
        # Extraire les chiffres
        prix_clean = re.sub(r'[^\d.]', '', prix_str)
        try:
            return float(prix_clean) if prix_clean else None
        except:
            return None
    
    df['Prix_Num'] = df['Prix'].apply(nettoyer_prix)
    df_clean = df[df['Prix_Num'].notna()].copy()
    
    if len(df_clean) == 0:
        return None
    
    # Convertir notes
    df_clean['Note_Num'] = pd.to_numeric(df_clean['Note'], errors='coerce')
    df_clean['Nb_Avis_Num'] = pd.to_numeric(df_clean['Nb_Avis'], errors='coerce')
    
    # Statistiques globales
    analyses['total_produits'] = len(df_clean)
    analyses['prix_moyen'] = df_clean['Prix_Num'].mean()
    analyses['prix_median'] = df_clean['Prix_Num'].median()
    analyses['prix_min'] = df_clean['Prix_Num'].min()
    analyses['prix_max'] = df_clean['Prix_Num'].max()
    
    # Produits les plus chers (top 10)
    analyses['top_chers'] = df_clean.nlargest(10, 'Prix_Num')[['Titre', 'Prix', 'Note', 'Nb_Avis']]
    
    # Produits les moins chers (top 10)
    analyses['top_moins_chers'] = df_clean.nsmallest(10, 'Prix_Num')[['Titre', 'Prix', 'Note', 'Nb_Avis']]
    
    # Produits les plus aimés (meilleure note et nb avis)
    df_notes = df_clean[df_clean['Note_Num'].notna() & df_clean['Nb_Avis_Num'].notna()].copy()
    if len(df_notes) > 0:
        df_notes['Score_Popularite'] = df_notes['Note_Num'] * df_notes['Nb_Avis_Num']
        analyses['top_aimes'] = df_notes.nlargest(10, 'Score_Popularite')[['Titre', 'Prix', 'Note', 'Nb_Avis']]
    
    # Distribution des prix
    analyses['df_clean'] = df_clean
    
    return analyses


def create_download_link(file_path, link_text):
    """Crée un lien de téléchargement"""
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    ext = file_path.suffix
    mime = 'text/csv' if ext == '.csv' else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return f'<a href="data:{mime};base64,{b64}" download="{file_path.name}" class="download-btn">⬇️ {link_text}</a>'


def show_sweet_alert(title, text, icon):
    """Affiche une alerte SweetAlert"""
    st.markdown(f"""
    <script>
        Swal.fire({{
            title: '{title}',
            text: '{text}',
            icon: '{icon}',
            confirmButtonColor: '#FF9900'
        }});
    </script>
    """, unsafe_allow_html=True)


# Interface Streamlit
def main():
    # Header
    st.markdown('<h1 class="main-header">🛒 Amazon Scraper Pro - Analyse Complète</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=200)
        st.markdown("---")
        
        menu = st.radio(
            "📋 Menu",
            ["🔍 Scraping", "📊 Consolidation & Analyse", "📁 Fichiers"]
        )
        
        st.markdown("---")
        st.markdown("""
        ### 💡 À propos
        Application de scraping Amazon avec:
        - Extraction automatique
        - Consolidation des données
        - Analyses descriptives
        - Export CSV & Excel
        """)
    
    # Page Scraping
    if menu == "🔍 Scraping":
        st.header("🔍 Nouveau Scraping")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            mot_cle = st.text_input("🔎 Mot-clé de recherche", "Thriller", key="mot_cle")
        
        with col2:
            nb_produits = st.number_input("📊 Nombre de produits", min_value=10, max_value=1000, value=100, step=10)
        
        with col3:
            max_pages = st.number_input("📄 Pages maximum", min_value=1, max_value=100, value=20, step=5)
        
        st.markdown("---")
        
        if st.button("🚀 Lancer le scraping", key="scrape_btn"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Scraping
            donnees = scraper(mot_cle, nb_produits, max_pages, progress_bar, status_text)
            
            if donnees:
                status_text.success(f"✅ {len(donnees)} produits collectés !")
                
                # Export
                csv_path, excel_path = exporter_scraping(donnees, mot_cle)
                
                # Affichage
                df_display = pd.DataFrame(donnees)
                st.dataframe(df_display, use_container_width=True)
                
                # Téléchargements
                st.markdown("### 📥 Télécharger les résultats")
                col1, col2 = st.columns(2)
                
                with col1:
                    with open(csv_path, 'rb') as f:
                        st.download_button(
                            "⬇️ Télécharger CSV",
                            f.read(),
                            csv_path.name,
                            "text/csv",
                            key="download_csv"
                        )
                
                with col2:
                    with open(excel_path, 'rb') as f:
                        st.download_button(
                            "⬇️ Télécharger Excel",
                            f.read(),
                            excel_path.name,
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download_excel"
                        )
                
                st.balloons()
    
    # Page Consolidation & Analyse
    elif menu == "📊 Consolidation & Analyse":
        st.header("📊 Consolidation & Analyse des Données")
        
        if st.button("🔄 Consolider tous les fichiers", key="consolidate_btn"):
            with st.spinner("Consolidation en cours..."):
                result = consolider_fichiers()
                
                if result and result[0]:
                    csv_path, excel_path, df_consolidated = result
                    
                    st.success(f"✅ Consolidation terminée ! {len(df_consolidated)} produits uniques")
                    
                    # Téléchargements fichier consolidé
                    st.markdown("### 📥 Télécharger le fichier consolidé")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        with open(csv_path, 'rb') as f:
                            st.download_button(
                                "⬇️ Télécharger CSV consolidé",
                                f.read(),
                                csv_path.name,
                                "text/csv",
                                key="download_consolidated_csv"
                            )
                    
                    with col2:
                        with open(excel_path, 'rb') as f:
                            st.download_button(
                                "⬇️ Télécharger Excel consolidé",
                                f.read(),
                                excel_path.name,
                                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="download_consolidated_excel"
                            )
                    
                    # Analyse
                    st.markdown("---")
                    st.header("📈 Analyse Descriptive")
                    
                    analyses = analyser_donnees(df_consolidated)
                    
                    if analyses:
                        # Métriques principales
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("📦 Total Produits", f"{analyses['total_produits']:,}")
                        
                        with col2:
                            st.metric("💰 Prix Moyen", f"${analyses['prix_moyen']:.2f}")
                        
                        with col3:
                            st.metric("💵 Prix Minimum", f"${analyses['prix_min']:.2f}")
                        
                        with col4:
                            st.metric("💎 Prix Maximum", f"${analyses['prix_max']:.2f}")
                        
                        st.markdown("---")
                        
                        # Graphiques
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📊 Distribution des Prix")
                            fig = px.histogram(
                                analyses['df_clean'],
                                x='Prix_Num',
                                nbins=50,
                                title="Distribution des Prix",
                                labels={'Prix_Num': 'Prix ($)', 'count': 'Nombre de produits'}
                            )
                            fig.update_traces(marker_color='#FF9900')
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            st.subheader("⭐ Distribution des Notes")
                            df_notes = analyses['df_clean'][analyses['df_clean']['Note_Num'].notna()]
                            if len(df_notes) > 0:
                                fig = px.histogram(
                                    df_notes,
                                    x='Note_Num',
                                    nbins=20,
                                    title="Distribution des Notes",
                                    labels={'Note_Num': 'Note', 'count': 'Nombre de produits'}
                                )
                                fig.update_traces(marker_color='#232F3E')
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Box plot prix
                        st.subheader("📦 Box Plot - Analyse des Prix")
                        fig = px.box(
                            analyses['df_clean'],
                            y='Prix_Num',
                            title="Analyse de la Distribution des Prix",
                            labels={'Prix_Num': 'Prix ($)'}
                        )
                        fig.update_traces(marker_color='#FF9900', boxmean='sd')
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.markdown("---")
                        
                        # Top produits
                        tab1, tab2, tab3 = st.tabs(["💎 Plus Chers", "💵 Moins Chers", "❤️ Plus Aimés"])
                        
                        with tab1:
                            st.subheader("💎 Top 10 - Produits les Plus Chers")
                            st.dataframe(analyses['top_chers'], use_container_width=True, hide_index=True)
                        
                        with tab2:
                            st.subheader("💵 Top 10 - Produits les Moins Chers")
                            st.dataframe(analyses['top_moins_chers'], use_container_width=True, hide_index=True)
                        
                        with tab3:
                            if 'top_aimes' in analyses:
                                st.subheader("❤️ Top 10 - Produits les Plus Aimés")
                                st.dataframe(analyses['top_aimes'], use_container_width=True, hide_index=True)
                            else:
                                st.info("Pas assez de données de notes et avis")
                    
                    st.balloons()
                else:
                    st.warning("⚠️ Aucun fichier à consolider. Effectuez d'abord un scraping.")
    
    # Page Fichiers
    else:
        st.header("📁 Gestion des Fichiers")
        
        tab1, tab2, tab3 = st.tabs(["📄 CSV", "📊 Excel", "🔄 Consolidés"])
        
        with tab1:
            st.subheader("📄 Fichiers CSV")
            csv_files = list(Config.CSV_DIR.glob("*.csv"))
            if csv_files:
                for f in csv_files:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f.name)
                    with col2:
                        with open(f, 'rb') as file:
                            st.download_button(
                                "⬇️",
                                file.read(),
                                f.name,
                                "text/csv",
                                key=f"csv_{f.name}"
                            )
            else:
                st.info("Aucun fichier CSV disponible")
        
        with tab2:
            st.subheader("📊 Fichiers Excel")
            excel_files = list(Config.EXCEL_DIR.glob("*.xlsx"))
            if excel_files:
                for f in excel_files:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f.name)
                    with col2:
                        with open(f, 'rb') as file:
                            st.download_button(
                                "⬇️",
                                file.read(),
                                f.name,
                                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"excel_{f.name}"
                            )
            else:
                st.info("Aucun fichier Excel disponible")
        
        with tab3:
            st.subheader("🔄 Fichiers Consolidés")
            consolidated_files = list(Config.CONSOLIDATED_DIR.glob("*"))
            if consolidated_files:
                for f in consolidated_files:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f.name)
                    with col2:
                        mime = "text/csv" if f.suffix == ".csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        with open(f, 'rb') as file:
                            st.download_button(
                                "⬇️",
                                file.read(),
                                f.name,
                                mime,
                                key=f"consolidated_{f.name}"
                            )
            else:
                st.info("Aucun fichier consolidé disponible")


if __name__ == "__main__":
    main()
