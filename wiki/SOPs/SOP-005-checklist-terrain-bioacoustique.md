# SOP-005 — Checklist Terrain Bioacoustique RPi 5

> **Objectif :** Garantir la connexion et la stabilité du Raspberry Pi 5 avec BirdNET-Go lors des sorties nature.
> **Public :** JCH (Consultation sur iPhone)
> **Statut :** V1.0 - 2026-05-24

---

## 🛑 1. Avant de partir (À la maison)

- [ ] **Alimentation :** Utiliser une Powerbank **USB-C PD (Power Delivery)** capable de 25W minimum (5V/5A).
  - *Note : Une batterie standard 2.4A provoquera des reboots ou des coupures Wi-Fi sur le RPi 5.*
- [ ] **Câble :** Utiliser un câble USB-C "Haute Puissance" (celui fourni avec le RPi ou un câble de charge Mac/iPad).
- [ ] **Mise à jour :** Lancer le RPi une fois sur le Wi-Fi maison pour vérifier que Tailscale est bien "Online".
- [ ] **Tailscale iPhone :** Ouvrir l'app Tailscale sur l'iPhone et vérifier que le VPN est "Connected".

## 📱 2. Configuration iPhone (Sur place)

- [ ] **Partage de connexion :** Activé.
- [ ] **Maximiser la compatibilité :** **ACTIVÉ** (Réglages > Partage de connexion). 
  - *Indispensable pour forcer le 2.4GHz et stabiliser la connexion du RPi.*
- [ ] **Garder l'écran allumé :** Rester sur la page "Partage de connexion" pendant que le RPi démarre (jusqu'à voir la barre bleue).

## 🦉 3. Démarrage du RPi

- [ ] Brancher le RPi à la batterie.
- [ ] Attendre ~90 secondes (le RPi 5 boote vite, mais BirdNET-Go prend du temps à charger le modèle IA).
- [ ] **Vérifier la connexion :** Regarder le haut de l'écran iPhone. 
  - Si **"1 connexion"** apparaît (bulle bleue/verte) -> Le RPi est sur le réseau.

## 🔗 4. Connexion à l'interface

- [ ] **Méthode A (Recommandée) :** Ouvrir l'app **Tailscale** > cliquer sur `birdnetpi` ou sur l'IP **100.84.45.93**.
- [ ] **Méthode B (Directe) :** Dans Safari, taper `http://100.84.45.93:8080`.
- [ ] **Méthode C (Secours) :** Taper `http://172.20.10.2:8080` (IP par défaut du hotspot).

## 🛠️ 5. Diagnostic rapide si ça ne marche pas

| Problème | Cause probable | Action |
| :--- | :--- | :--- |
| Pas de "1 connexion" sur iPhone | SSID/MDP Wi-Fi incorrect ou 5GHz | Activer "Maximiser la compatibilité" + Vérifier le MDP. |
| Connexion intermittente | Puissance batterie trop faible | Changer de port sur la batterie ou changer de câble. |
| Page blanche dans Safari | BirdNET-Go encore en train de booter | Attendre 1 minute de plus. |
| Tailscale "Offline" | VPN iPhone coupé | Réactiver Tailscale sur l'iPhone. |

---
*Règle Dobby : Toujours privilégier l'IP Tailscale pour s'affranchir des caprices du mDNS Apple sur hotspot.*
