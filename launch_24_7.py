#!/usr/bin/env python3
"""
🚀 BOT VINTED 24/7 - CHASSEUR DE PÉPITES CONTINU
===============================================

Ce bot tourne EN CONTINU 24h/24 7j/7 pour trouver les meilleures affaires Vinted.

FONCTIONNALITÉS:
- ♾️  Scan INFINI sans arrêt
- 🎯 Évite les doublons (jamais 2x le même article)
- 📱 Notifications Telegram instantanées
- 🔄 Redémarrage automatique en cas d'erreur
- 💎 Recherche élargie sur toutes les stratégies
- 🎲 Ordre aléatoire pour optimiser les découvertes

UTILISATION:
python launch_24_7.py
"""

import sys
import os
from bot_24_7 import VintedBot24_7

def check_dependencies():
    """Vérifier les dépendances"""
    try:
        import selenium
        import perplexity
        print("✅ Dépendances OK")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Exécutez: pip install -r requirements.txt")
        return False

def main():
    print("""
    🚀 BOT VINTED 24/7 - CHASSEUR DE PÉPITES
    ========================================
    
    ♾️  FONCTIONNEMENT CONTINU:
    - Scan infini sans arrêt
    - Jamais le même article 2 fois
    - Notifications Telegram instantanées
    - Redémarrage auto en cas d'erreur
    
    💎 STRATÉGIES ACTIVES:
    - 💎 ERREURS DE PRIX LUXE (max 40€)
    - 🏆 VINTAGE GOLDMINE (max 20€)
    - 👟 SNEAKERS STEALS (max 80€)
    
    📱 TELEGRAM: Activé (notifications instantanées)
    🔄 ROTATION: Marques et stratégies aléatoires
    """)
    
    if not check_dependencies():
        return
    
    print("\n⚠️  ATTENTION:")
    print("Ce bot va tourner EN CONTINU jusqu'à ce que vous l'arrêtiez (Ctrl+C)")
    print("Il va consommer des ressources et faire de nombreuses requêtes.")
    
    confirm = input("\n🚀 Lancer le bot 24/7 ? (oui/non): ").strip().lower()
    
    if confirm not in ['oui', 'o', 'yes', 'y']:
        print("❌ Lancement annulé")
        return
    
    print("\n🔥 LANCEMENT DU BOT 24/7...")
    print("💡 Appuyez sur Ctrl+C pour arrêter")
    print("="*50)
    
    try:
        bot = VintedBot24_7()
        bot.run_continuous_scan()
    except KeyboardInterrupt:
        print("\n🛑 Bot arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur critique: {e}")

if __name__ == "__main__":
    main()