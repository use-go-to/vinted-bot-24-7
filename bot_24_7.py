import perplexity
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re
import urllib.parse
from datetime import datetime
import random
from config import *
from marque_rotator import MarqueRotator
from telegram_bot import TelegramBot

class VintedBot24_7:
    def __init__(self):
        self.ai_client = perplexity.Client()
        self.memory = self.load_memory()
        self.driver = None
        self.opportunities = []
        self.telegram = TelegramBot(TELEGRAM_CONFIG.get('token'), TELEGRAM_CONFIG.get('chat_id'))
        self.rotator = MarqueRotator()
        self.analyzed_articles = set()  # Éviter les doublons
        self.scan_count = 0
        
    def load_memory(self):
        try:
            with open(CASCADE_CONFIG['memory_file'], 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_memory(self):
        with open(CASCADE_CONFIG['memory_file'], 'w') as f:
            json.dump(self.memory, f)
    
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        return webdriver.Chrome(options=options)
    
    def build_url(self, marque, prix_max, etats):
        params = {
            'search_text': marque,
            'price_to': prix_max,
            'currency': 'EUR',
            'order': 'newest_first',
            'status_ids[]': etats
        }
        query = urllib.parse.urlencode(params, doseq=True)
        return f"{VINTED_URLS['france']}?{query}"
    
    def extract_id(self, url):
        match = re.search(r'/items/(\d+)', url)
        return match.group(1) if match else None
    
    def scan_articles(self, url):
        try:
            self.driver.get(url)
            
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                ).click()
            except:
                pass
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/items/"]'))
            )
            
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/items/"]')
            new_articles = []
            
            for link in links[:30]:  # Analyser plus d'articles
                href = link.get_attribute("href")
                if not href or "/items/" not in href:
                    continue
                
                if any(x in href for x in ["promoted", "ad", "sponsor"]):
                    continue
                
                item_id = self.extract_id(href)
                if not item_id or item_id in self.analyzed_articles:
                    continue
                
                self.analyzed_articles.add(item_id)
                new_articles.append({
                    'id': item_id,
                    'url': href.split('?')[0]
                })
                
                if len(new_articles) >= 15:  # Plus d'analyses
                    break
            
            return new_articles
            
        except Exception as e:
            print(f"❌ Erreur scan: {e}")
            return []
    
    def extract_data(self, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'h1'))
            )
            
            script = """
            return {
                titre: document.querySelector('h1')?.textContent?.trim() || 'N/A',
                prix: document.querySelector('p[class*="subtitle"]')?.textContent?.trim() || 'N/A',
                marque: document.querySelector('span[itemprop="name"]')?.textContent?.trim() || 'N/A',
                etat: document.querySelector('div[itemprop="status"] span')?.textContent?.trim() || 'N/A',
                taille: document.querySelector('div[itemprop="size"] span')?.textContent?.trim() || 'N/A'
            };
            """
            
            data = self.driver.execute_script(script)
            data['url'] = url
            return data
            
        except:
            return None
    
    def ai_analyze(self, item, strategie):
        prompt = AI_CONFIG['prompt_template'].format(
            titre=item.get('titre', 'N/A'),
            prix=item.get('prix', 'N/A'),
            marque=item.get('marque', 'N/A'),
            etat=item.get('etat', 'N/A'),
            taille=item.get('taille', 'N/A'),
            strategie_nom=strategie['nom'],
            prix_max=strategie['prix_max']
        )
        
        try:
            response = self.ai_client.search(prompt, mode=AI_CONFIG['mode'])
            analysis = response.get('answer', '')
            
            score_match = re.search(r'SCORE:\s*(\d+)', analysis)
            achat_match = re.search(r'ACHAT:\s*(OUI|NON)', analysis)
            marge_match = re.search(r'MARGE:\s*(\d+)', analysis)
            prix_vente_match = re.search(r'PRIX_VENTE:\s*(\d+)', analysis)
            
            score = int(score_match.group(1)) if score_match else 0
            achat = achat_match.group(1) if achat_match else 'NON'
            marge = int(marge_match.group(1)) if marge_match else 0
            prix_vente = int(prix_vente_match.group(1)) if prix_vente_match else 0
            
            return {
                'score': score,
                'achat': achat,
                'analysis': analysis,
                'marge_nette': marge,
                'prix_vente': prix_vente
            }
            
        except Exception as e:
            return {'score': 0, 'achat': 'NON', 'analysis': f'Erreur: {e}', 'marge_nette': 0, 'prix_vente': 0}
    
    def process_opportunity(self, opportunity):
        """Traiter une opportunité trouvée"""
        self.opportunities.append(opportunity)
        
        # Envoi Telegram immédiat
        if TELEGRAM_CONFIG.get('enabled', False):
            self.telegram.send_opportunity(opportunity)
        
        # Log dans fichier
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_text = f"🎯 PÉPITE TROUVÉE - {timestamp}\n"
        log_text += f"Score: {opportunity['score']}/10 | Marge: {opportunity['marge_nette']}€\n"
        log_text += f"Article: {opportunity['data']['titre'][:50]}...\n"
        log_text += f"URL: {opportunity['data']['url']}\n"
        log_text += "-" * 60 + "\n"
        
        with open(f"pepites_{datetime.now().strftime('%Y%m%d')}.txt", 'a', encoding='utf-8') as f:
            f.write(log_text)
        
        print(f"💎 PÉPITE! Score: {opportunity['score']}/10 | {opportunity['data']['titre'][:40]}...")
    
    def run_continuous_scan(self):
        """Bot 24/7 CONTINU"""
        print("🚀 BOT VINTED 24/7 - DÉMARRAGE CONTINU")
        print("="*50)
        print("⚡ Le bot ne s'arrêtera JAMAIS")
        print("💎 Recherche de pépites en continu...")
        print("📱 Notifications Telegram instantanées")
        print("="*50)
        
        while True:
            try:
                self.scan_count += 1
                print(f"\n🔄 SCAN #{self.scan_count} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Redémarrer le driver périodiquement
                if self.scan_count % 20 == 1:
                    if self.driver:
                        self.driver.quit()
                    self.driver = self.setup_driver()
                    print("🔄 Driver redémarré")
                
                strategies = list(STRATEGIES_CONFIG.values())
                random.shuffle(strategies)  # Ordre aléatoire
                
                for strategie in strategies:
                    marques = strategie['marques'].copy()
                    random.shuffle(marques)  # Marques aléatoires
                    
                    for marque in marques[:2]:  # 2 marques par stratégie
                        url = self.build_url(marque, strategie['prix_max'], strategie['etats'])
                        articles = self.scan_articles(url)
                        
                        for article in articles[:5]:  # 5 articles max par marque
                            data = self.extract_data(article['url'])
                            if not data:
                                continue
                            
                            ai_result = self.ai_analyze(data, strategie)
                            
                            if ai_result['score'] >= strategie['score_min'] and ai_result['achat'] == 'OUI':
                                opportunity = {
                                    'timestamp': time.time(),
                                    'strategie': strategie['nom'],
                                    'marque': marque,
                                    'score': ai_result['score'],
                                    'achat': ai_result['achat'],
                                    'data': data,
                                    'analysis': ai_result['analysis'],
                                    'marge_nette': ai_result['marge_nette'],
                                    'prix_vente': ai_result['prix_vente']
                                }
                                
                                self.process_opportunity(opportunity)
                            
                            time.sleep(0.3)  # Délai court
                        
                        time.sleep(1)  # Pause entre marques
                
                # Pause entre cycles complets
                pause = random.randint(30, 60)  # 30-60 secondes
                print(f"⏳ Pause {pause}s avant prochain cycle...")
                time.sleep(pause)
                
            except KeyboardInterrupt:
                print("\n🛑 Arrêt demandé par l'utilisateur")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")
                print("🔄 Redémarrage dans 10 secondes...")
                time.sleep(10)
                continue
        
        if self.driver:
            self.driver.quit()
        
        print(f"\n📊 STATISTIQUES FINALES:")
        print(f"🔍 Scans effectués: {self.scan_count}")
        print(f"💎 Pépites trouvées: {len(self.opportunities)}")
        print(f"📱 Articles analysés: {len(self.analyzed_articles)}")

def main():
    bot = VintedBot24_7()
    bot.run_continuous_scan()

if __name__ == "__main__":
    main()