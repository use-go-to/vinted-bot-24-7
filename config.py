# ==========================================
# CONFIGURATION AVANCÉE VINTED AI OPTIMIZER
# ==========================================

# Stratégies ULTRA-PRÉCISES basées sur les vraies bonnes affaires
STRATEGIES_CONFIG = {
    "erreurs_prix_luxe": {
        "nom": "💎 ERREURS DE PRIX LUXE",
        "marques": [
            "Stone Island", "Moncler", "Canada Goose", "Arc'teryx", 
            "Patagonia", "The North Face", "Acne Studios", "Maison Margiela"
        ],
        "prix_max": 40,
        "etats": [6, 1, 2],
        "score_min": 6,  # Baissé pour plus d'opportunités
        "priorite": 1,
        "tailles_adultes": ["S", "M", "L", "XL", "XXL"],
        "mots_cles_exclus": ["enfant", "junior", "kid", "baby", "6 ans", "8 ans", "10 ans", "12 ans", "14 ans", "16 ans"]
    },
    
    "vintage_goldmine": {
        "nom": "🏆 VINTAGE GOLDMINE",
        "marques": [
            "Polo Ralph Lauren", "Tommy Hilfiger", "Lacoste", "Burberry",
            "Carhartt WIP", "Dickies", "Champion", "Nike Vintage"
        ],
        "prix_max": 20,
        "etats": [6, 1, 2],
        "score_min": 6,  # Baissé pour plus d'opportunités
        "priorite": 1,
        "tailles_adultes": ["S", "M", "L", "XL", "XXL"],
        "mots_cles_exclus": ["enfant", "junior", "kid", "baby"]
    },
    
    "sneakers_steals": {
        "nom": "👟 SNEAKERS STEALS",
        "marques": [
            "Jordan 1", "Jordan 4", "Dunk Low", "Air Force 1",
            "New Balance 550", "Adidas Samba", "Yeezy 350", "Travis Scott"
        ],
        "prix_max": 80,
        "etats": [6, 1, 2],
        "score_min": 6,  # Baissé pour plus d'opportunités
        "priorite": 2,
        "tailles_adultes": ["40", "41", "42", "43", "44", "45", "46"],
        "mots_cles_exclus": ["enfant", "junior", "kid", "baby"]
    }
}

# Configuration IA GPT-4O OPTIMISÉE (Gratuit mais ultra-précis)
AI_CONFIG = {
    "mode": "auto",  # Mode gratuit
    "prompt_template": """
EXPERT VINTED - ANALYSE ULTRA-PRÉCISE

ARTICLE :
{titre}
Prix: {prix} | Marque: {marque} | État: {etat} | Taille: {taille}

RÈGLES STRICTES :
1. ADULTE SEULEMENT - Rejeter si enfant/junior/kid/6ans/8ans/10ans
2. TAILLES ADULTES - S,M,L,XL pour vêtements / 40-46 pour chaussures
3. MARGE MINIMUM 25€ - Sinon REJET automatique

PRIX MARCHÉ VINTED (données réelles) :
- Stone Island sweat: 80-120€
- Moncler doudoune: 150-300€  
- Ralph Lauren polo: 25-45€
- Carhartt WIP: 40-70€
- Jordan 4: 120-200€
- Dunk Low: 80-150€

CALCUL MARGE :
Prix vente - Prix achat - Frais Vinted (5% + 0,70€) = Marge nette

EXEMPLE :
Stone Island 35€ → Vente 100€ → Frais 5,70€ → Marge: 59€ = EXCELLENT

RÉPONDS EXACTEMENT :
ADULTE: OUI/NON
TAILLE_OK: OUI/NON  
PRIX_VENTE: XXX€
MARGE: XX€
DEMANDE: FORTE/MOYENNE/FAIBLE
SCORE: X/10
ACHAT: OUI/NON
""",
    
    "retry_attempts": 2,
    "timeout": 10
}

# Configuration Selenium ÉLARGIE
SELENIUM_CONFIG = {
    "headless": True,
    "timeout": 15,  # Plus de temps
    "max_articles_per_search": 10,  # Doublé
    "delay_between_requests": 0.5,   # Plus rapide
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Configuration système CASCADE ÉLARGI
CASCADE_CONFIG = {
    "memory_file": "last_seen_ids.json",
    "max_new_articles": 20,  # Doublé pour plus d'analyses
    "scan_interval": 300,
    "save_opportunities": True,
    "alert_threshold": 6     # Baissé pour plus d'alertes
}

# URLs de base Vinted par pays
VINTED_URLS = {
    "france": "https://www.vinted.fr/catalog",
    "belgique": "https://www.vinted.be/catalog", 
    "espagne": "https://www.vinted.es/catalog",
    "italie": "https://www.vinted.it/catalog"
}

# Configuration notifications Telegram
TELEGRAM_CONFIG = {
    "enabled": True,  # ✅ ACTIVÉ
    "token": "8476385296:AAHUevAk3BaQB7b8udRh-WtNWADVoIT9YEQ",
    "chat_id": "5756465712"
}