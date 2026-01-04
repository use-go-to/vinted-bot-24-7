import json
import random
from datetime import datetime, timedelta

class MarqueRotator:
    def __init__(self):
        self.rotation_file = "marque_rotation.json"
        self.rotation_data = self.load_rotation()
    
    def load_rotation(self):
        """Charger les données de rotation"""
        try:
            with open(self.rotation_file, 'r') as f:
                return json.load(f)
        except:
            return {
                "last_scanned": {},
                "performance": {},
                "blacklist": []
            }
    
    def save_rotation(self):
        """Sauvegarder les données de rotation"""
        with open(self.rotation_file, 'w') as f:
            json.dump(self.rotation_data, f, indent=2)
    
    def should_scan_marque(self, marque, strategie_nom):
        """Déterminer si on doit scanner cette marque"""
        key = f"{strategie_nom}_{marque}"
        
        # Vérifier blacklist temporaire
        if marque in self.rotation_data.get("blacklist", []):
            return False
        
        # Vérifier dernière fois scannée
        last_scan = self.rotation_data["last_scanned"].get(key)
        if last_scan:
            last_time = datetime.fromisoformat(last_scan)
            # Attendre au moins 2h entre scans de la même marque
            if datetime.now() - last_time < timedelta(hours=2):
                return False
        
        return True
    
    def mark_scanned(self, marque, strategie_nom, found_items=0):
        """Marquer une marque comme scannée"""
        key = f"{strategie_nom}_{marque}"
        self.rotation_data["last_scanned"][key] = datetime.now().isoformat()
        
        # Tracker performance
        if key not in self.rotation_data["performance"]:
            self.rotation_data["performance"][key] = {"scans": 0, "items": 0}
        
        self.rotation_data["performance"][key]["scans"] += 1
        self.rotation_data["performance"][key]["items"] += found_items
        
        # Blacklist si trop de scans sans résultats
        perf = self.rotation_data["performance"][key]
        if perf["scans"] >= 10 and perf["items"] == 0:
            if marque not in self.rotation_data["blacklist"]:
                self.rotation_data["blacklist"].append(marque)
                print(f"🚫 {marque} ajoutée à la blacklist (0 résultat en 10 scans)")
        
        self.save_rotation()
    
    def get_priority_marques(self, marques, strategie_nom):
        """Obtenir les marques par ordre de priorité"""
        available = [m for m in marques if self.should_scan_marque(m, strategie_nom)]
        
        if not available:
            # Si aucune marque disponible, prendre les plus anciennes
            available = marques[:3]
        
        # Mélanger pour éviter toujours le même ordre
        random.shuffle(available)
        
        # Limiter à 3 marques par stratégie pour optimiser
        return available[:3]
    
    def reset_blacklist(self):
        """Reset blacklist (à faire périodiquement)"""
        self.rotation_data["blacklist"] = []
        self.save_rotation()
        print("🔄 Blacklist réinitialisée")