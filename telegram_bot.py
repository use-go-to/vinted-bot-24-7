import requests
import json
from datetime import datetime

class TelegramBot:
    def __init__(self, token=None, chat_id=None):
        self.token = token
        self.chat_id = chat_id
        self.enabled = token and chat_id
        
    def send_message(self, text):
        """Envoyer message Telegram"""
        if not self.enabled:
            return False
            
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def send_opportunity(self, opportunity):
        """Envoyer opportunité formatée avec prix et marge"""
        data = opportunity['data']
        marge = opportunity.get('marge_nette', 0)
        prix_vente = opportunity.get('prix_vente', 0)
        
        message = f"""
💎 <b>ERREUR DE PRIX LUXE DÉTECTÉE!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 <b>RENTABILITÉ:</b>
💰 Prix achat: <b>{data.get('prix', 'N/A')}</b>
💵 Prix revente: <b>{prix_vente}€</b>
🚀 <b>MARGE NETTE: {marge}€</b>

📦 <b>ARTICLE:</b>
{data.get('titre', 'N/A')[:80]}...

🏷️ <b>DÉTAILS:</b>
🏪 Marque: <b>{data.get('marque', 'N/A')}</b>
⭐ État: {data.get('etat', 'N/A')}
📏 Taille: {data.get('taille', 'N/A')}
📊 Score IA: <b>{opportunity['score']}/10</b>
🔥 Demande: {opportunity.get('demande', 'MOYENNE')}

🔗 <a href="{data.get('url', '')}">ACHETER MAINTENANT</a>

⏰ {datetime.now().strftime('%H:%M:%S')}
        """
        
        return self.send_message(message.strip())