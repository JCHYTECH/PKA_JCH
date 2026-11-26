# Ressources Home Assistant — Apprentissage & Référence

> Créé : 2026-07-19 | Dobby 🦉 — suite à la session iPhone/Sensor Logger/HA

---

## 📖 Guides débutant (FR)

1. **[Home Assistant pour les nuls](https://www.domo-blog.fr/home-assistant-pour-les-nuls-guide-demarrage-complet-pour-bien-commencer/)** — Domo-Blog  
   Le meilleur point d'entrée. Concepts clés (entités, intégrations, automatisations) expliqués simplement, sans jargon.

2. **[Bien débuter avec Home Assistant](https://forumdomotique.com/guides-tutoriels/home-assistant/bien-debuter-home-assistant/)** — Forum Domotique  
   Plus complet : installation, appareils compatibles, automatisations, dashboards, assistants vocaux.

3. **[Guide Ultime Domotique 2025](https://www.frichtiweb.com/templates/guides-tutoriels/ha/home-assistant-guide-debutant-domotique/)** — Frichtiweb  
   Approche pas-à-pas, mise à jour 2025.

4. **[Guide Complet Débuter](https://www.ladomotiquepourtous.com/guide-complet-pour-debuter-avec-home-assistant)** — La Domotique Pour Tous  
   Conseils pratiques pour une première installation réussie.

---

## 🎥 Vidéos (FR)

- **[Léo TechMaker](https://www.youtube.com/@Leo-TechMaker)** — excellente série HA en français
- Chercher « Home Assistant débutant » sur YouTube

## 🎥 Vidéos (EN)

- **[Everything Smart Home](https://www.youtube.com/@EverythingSmartHome)** — la référence anglophone
- Sous-titres FR disponibles sur beaucoup de vidéos

---

## 📚 Référence officielle

- **[Documentation officielle](https://www.home-assistant.io/docs/)** — la source ultime pour les intégrations spécifiques
- **[Community Forum](https://community.home-assistant.io/)** — résolution de problèmes

---

## 🧠 Architecture mentale (les 3 couches à retenir)

| Couche | Ce que c'est | Exemple dans PKA |
|---|---|---|
| **Intégrations** | Le tuyau qui connecte HA au monde extérieur | MQTT, Zigbee2MQTT, ZHA, Ecowitt |
| **Appareils / Entités** | Ce que HA voit et mesure | `sensor.esneux_pression_atmospherique`, LuxSerre |
| **Automatisations** | Ce que HA fait avec ces données | Alerte fuite d'eau, régulation serre, notif pression |

---

## 🔗 Fichiers liés dans PKA

- `JCH_Inbox/03_PROJECTS/11_IOT/_shared/ARCHITECTURE-MQTT-DISCOVERY.md` — comment les capteurs arrivent dans HA
- `scripts/pka_mqtt_discovery_bridge.py` — pont MQTT Discovery générique
- `scripts/pka_sensorlog_http_bridge.py` — pont HTTP→MQTT pour Sensor Logger
