# CONCORDANCE — Lupo Caméras ↔ WildNexus
> Dobby 🦉 — DeepSeek TUI — 2026-07-04
> Projets croisés : Caméras Van Lupo × WildNexus P0

---

## 1. Synthèse

Lupo (caméras de surveillance van) et WildNexus (caméra-piège faune) partagent **le même socle technique** — ESP32, caméras extérieures, alimentation solaire, boîtier IP67, pilotage par capteurs. Les deux projets peuvent s'enrichir mutuellement, et Lupo peut devenir la **gateway mobile** de WildNexus.

---

## 2. Ponts techniques — ce que WildNexus apporte à Lupo

| Compétence WildNexus | Application Lupo | Gain |
|----------------------|------------------|------|
| **Power gating MOSFET** — coupure totale du rail caméra | Remplacer le relais 5V par un MOSFET — plus compact, pas de clic, pas d'usure | Fiabilité ×10 |
| **PIR EKMB 2µA** — détection de mouvement ultra-basse conso | Remplacer OBD2 pour le déclenchement bivouac : PIR dans le boîtier ESP32 | Détection locale, pas de BT OBD2 |
| **Buck TPS62840 60nA Iq** — régulateur nano-ampère | Alimenter l'ESP32 depuis le 12V avec une conso veille quasi nulle | Autonomie batterie auxiliaire |
| **Deep sleep + wake timer** — pattern maîtrisé sur ESP32-S3 | ESP32 se réveille toutes les 30s pour vérifier état, sinon deep sleep | Conso veille divisée par 100 |
| **OV5640 + M12 lens** — hardware validé | Upgrade des caméras génériques vers un capteur connu et maîtrisé | Qualité d'image, coût connu |
| **Hammond 1554A IP67** — boîtier éprouvé | Boîtier pour l'électronique extérieure | Étanchéité validée |

## 3. Ponts inverses — ce que Lupo apporte à WildNexus

| Compétence Lupo | Application WildNexus | Gain |
|-----------------|----------------------|------|
| **Home Assistant embarqué** — RPi 5 + HA OS | Dashboard WildNexus mobile, alertes, visualisation | Interface utilisateur terrain |
| **Solar powerbank Pass-Through** — Xtorm/Sandberg | Option d'alimentation simplifiée pour tests rapides | Prototypage accéléré |
| **ESPHome OTA** — flash et mise à jour sans fil | WildNexus pourrait utiliser ESPHome au lieu du firmware bare-metal | Déploiement plus simple |
| **Van comme gateway LoRa** — RPi + antenne | Le van reçoit les données LoRa des nœuds WildNexus déployés autour du camp | Infrastructure mobile |

## 4. Vision long terme — Van = Station de Base WildNexus

```
  Campagne / Bivouac
  ┌─────────────────────────────────────────┐
  │  Nœud WN-1    Nœud WN-2    Nœud WN-3   │
  │  (arbre 50m)  (mare 200m)  (lisière)   │
  │      │            │            │        │
  │      └────────────┼────────────┘        │
  │              LoRa 868 MHz               │
  │                   │                     │
  │          ┌────────┴────────┐            │
  │          │   LUPO (Van)    │            │
  │          │ RPi 5 + HA +    │            │
  │          │ Passerelle LoRa │            │
  │          │ Dashboard local │            │
  │          └────────┬────────┘            │
  │                   │ LTE (optionnel)     │
  └───────────────────┼─────────────────────┘
                      ▼
              Smartphone JC
```

## 5. Actions P0 immédiates

### 🔴 P0 — Unifier le hardware ESP32

- **Action** : Adopter le MOSFET power-gating WildNexus (SI2302CDS) au lieu du relais 5V pour Lupo
- **Gain** : Circuit plus fiable, silencieux, plus compact
- **Responsable** : Forge 🔨

### 🔴 P0 — Ajouter un PIR au boîtier ESP32 Lupo

- **Action** : Intégrer un PIR Panasonic EKMB dans le boîtier Plexo pour le déclenchement bivouac
- **Gain** : Supprime la dépendance OBD2 pour la détection de présence
- **Responsable** : Araignée 🕷️ + Forge 🔨

### 🟡 P1 — Tester ESPHome sur WildNexus

- **Action** : Flasher un ESP32-S3 WildNexus avec ESPHome, mesurer la conso veille
- **Gain** : OTA, intégration HA native, courbe d'apprentissage partagée
- **Responsable** : Musaraigne 🦇

### 🟡 P1 — Préparer la gateway LoRa van

- **Action** : Ajouter un module LoRa RAK3172 au RPi 5 du van, configurer la réception
- **Gain** : Le van devient station de base WildNexus
- **Responsable** : Chouette 🦉 + Forge 🔨

---

## 6. Conclusion

**Les deux projets ne sont pas voisins — ils sont la face urbaine et la face sauvage du même système.** Lupo est un WildNexus qui regarde les humains au lieu des animaux. La stack technique est identique (ESP32 + caméra + solaire + IP67 + HA), seul le classifieur change (intrusion vs espèce).

**Recommandation** : ne pas traiter Lupo comme un projet séparé. Le rattacher à WildNexus comme "variante surveillance humaine", partager le hardware, les skills, et la BOM.
