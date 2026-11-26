# Concordance sonification.rtf ↔ LEAFNET v0.1

> **Date :** 2026-06-23
> **Source :** `JCH_Inbox/00_INBOX/sonification.rtf` (Note Apple Notes JC)
> **Auteur :** Dobby 🦉
> **Destinataires :** Forge 🔨, Araignée 🕷️ (LEAFNET)

---

## Résumé

Le document `sonification.rtf` est un guide technique complet pour le nœud bioélectrique végétal. Il couvre le même périmètre que le scope LEAFNET v0.1 mais avec un **niveau de détail d'implémentation** (code C++ prêt à compiler, schéma de câblage PPK2, optimisations deep sleep) là où LEAFNET reste au niveau conceptuel.

## Apports du document

### 1. Choix d'amplificateur — divergence à résoudre

| Document | Ampli recommandé | Type | CMRR | Prix |
|----------|-----------------|------|------|------|
| **LEAFNET v0.1** | AD623ANZ | Instrumentation | 110 dB | ~8€ |
| **sonification.rtf** | TLC2272 ou INA126 | AOP haut-Z / Instr. | ~80 dB / 94 dB | ~2€ / ~5€ |

**Analyse :** L'AD623 est supérieur aux deux alternatives citées (CMRR 110 dB vs 94 dB max). Pour les signaux µV des plantes en environnement bruyant, le CMRR est critique. **Recommandation : garder AD623ANZ**, mentionner INA126 comme alternative budget.

### 2. Plateforme — convergence XIAO

Les deux documents convergent sur **Seeed Studio XIAO** comme plateforme de déploiement. Le sonification.rtf va plus loin :

| Aspect | LEAFNET v0.1 | sonification.rtf |
|--------|-------------|-----------------|
| Modèle | XIAO ESP32C3 | XIAO ESP32-S3 **ou** C3 |
| Deep sleep | Mentionné | **44 µA mesuré** |
| Charge LiPo | Mentionnée | PMIC intégré documenté |
| PPK2 | Non mentionné | **Procédure complète** |

### 3. Firmware — code production-ready

Le sonification.rtf fournit **deux firmware complets et fonctionnels** :

- **Émetteur (capteur plante) :** 5 optimisations deep sleep documentées, ESP-NOW, structure de paquet extensible (`id` + `tensionPlante`)
- **Récepteur (hub central) :** callback asynchrone, décodage multi-capteurs par `id`

LEAFNET v0.1 n'a que des spécifications conceptuelles pour le firmware. Ce code est le point de départ immédiat pour le proto v0.1.

### 4. Optimisations deep sleep — nouveau pour LEAFNET

5 optimisations non documentées dans LEAFNET :

1. **CPU 80 MHz** — réduit la conso de 2× pendant la mesure
2. **Délai stabilisation 15 ms** — à valider au PPK2 (au lieu de délais arbitraires)
3. **Démarrage radio agressif** — WiFi STA + esp_now_init en < 100 ms
4. **VDDSDIO off en deep sleep** — coupe l'alimentation flash externe
5. **gpio_hold_en()** — empêche les fuites de courant vers l'AOP pendant le sommeil

### 5. ESP-NOW — code complet vs. mention

LEAFNET mentionne ESP-NOW comme option. Le sonification.rtf livre le **code complet émetteur + récepteur**, testé architecturalement. Intégration directe dans `02_FIRMWARE/`.

### 6. Intégration Home Assistant — nouvelle perspective

Le sonification.rtf ouvre une piste non explorée dans LEAFNET : **MQTT → Home Assistant via ESPHome**. La plante devient un capteur domotique. Le hub ESP32 fait passerelle ESP-NOW → MQTT → HA. Alignement parfait avec notre architecture HA distribuée (M5 + Esneux + van).

## Recommandations

### Action immédiate

1. **[Forge]** Copier le code firmware émetteur dans `LEAFNET/02_FIRMWARE/emitter-espnow/`
2. **[Forge]** Copier le code firmware récepteur dans `LEAFNET/02_FIRMWARE/hub-espnow/`
3. **[Araignée]** Valider les 5 optimisations deep sleep au PPK2 (procédure documentée dans le .rtf)
4. **[Dobby]** Mettre à jour `leafnet-v0.1-scope.md` avec les enrichissements ci-dessous

### Enrichissements du scope LEAFNET

| Section actuelle | Enrichissement |
|-----------------|---------------|
| 2.1 Hardware | Ajouter TLC2272 et INA126 comme alternatives budget à AD623 |
| 2.2 Firmware | Référencer le code ESP-NOW fourni par sonification.rtf |
| 3.3 Intégration | Ajouter MQTT → Home Assistant (ESPHome) |
| 6. Roadmap | Ajouter PPK2 comme outil de validation pour chaque phase |

### Routage fichier

- **Source :** `JCH_Inbox/00_INBOX/sonification.rtf`
- **Destination :** `NEXUS_ACOUSTIC/LEAFNET/99_REFERENCES/sonification-iot-vegetal-esp32.rtf`
- **Conversion :** `.md` également sauvegardé pour référence rapide

---

*Analyse de concordance. Le sonification.rtf transforme LEAFNET de « concept validé » à « prêt à prototyper ».*
