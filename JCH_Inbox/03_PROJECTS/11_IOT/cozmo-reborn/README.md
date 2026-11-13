# Cozmo Reborn — Compagnon IA local 🦉

> **Objectif** : transformer le Cozmo (Anki) en **compagnon IA incarné**, avec un cerveau **local** (M1/Ollama), en réutilisant les leçons du revival Karotz.
> **Projet ombrelle** : `11_IOT` · **Hub** : M5 (hôte SDK) + M1 (cerveau Ollama) · liaison Tailscale.
> **Statut** : ⚪ en préparation — analyse faite, matériel à recenser, premier PoC à définir.
> **Source** : analyse Dobby 2026-11-09/10 + `../karotz-reborn/resurrection-karotz-2026-11-09.md`.

---

## Vision

Même schéma que le Karotz (objet « bête » + cerveau local), mais plus riche :

- **yeux** : caméra du Cozmo → vision locale (`gemma3:27b`) → il « reconnaît » gens/objets
- **voix** : TTS local → le robot parle
- **visage** : écran facial + expressions (émotion)
- **corps** : chenilles + bras (déplacements, gestes)
- **cerveau** : **local** (M1 Ollama), zéro cloud DDL — cohérent avec le « zéro cloud / zéro abonnement » du projet IOT

---

## La contrainte clé du Cozmo (le gros écart avec le Karotz)

Le Cozmo **n'a pas de cerveau à bord** : sa vision, son « moteur d'émotion » et ses animations tournent sur le **téléphone/tablette appairé** (app Cozmo). Le robot n'est que caméra + moteurs + écran facial.

→ Le Karotz se pilote par **flash USB + interface web locale** (OpenKarotz). Le Cozmo, lui, se pilote par **SDK Python** (officiel Anki, package `cozmo`) qui dialogue avec **l'app Cozmo** ouverte sur un téléphone. C'est le principal changement à anticiper.

---

## Leçons du Karotz — appliquées au Cozmo

| Leçon Karotz | Transposition Cozmo | Action |
|---|---|---|
| WiFi **WPA (TKIP)** + 802.11g obligatoire (le WPA2 seul bloque) | Cozmo = WiFi **2,4 GHz uniquement** (comme la plupart des robots Anki), appairage par l'app | Vérifier un SSID **2,4 GHz** disponible AVANT l'appairage (le RUT240 peut émettre un réseau dédié) |
| Clé USB à **retirer après flash** (sinon réinstallation + config écrasée) | Pas de clé, mais le robot doit rester **appairé** ; l'app est le point de passage | Repérer la procédure de **reset/appairage** et ses pièges |
| Serveur web qui ne démarre pas (inetd figé) | Le SDK dépend de **l'app ouverte** + serveur SDK | Vérifier que l'app + le SDK tournent et restent actifs |
| Firmware corrompu après coupure (MAC aléatoire) | Firmware du robot géré par l'app DDL | **Ne pas couper l'alim** pendant une mise à jour |
| Cerveau **déporté** (le lapin est trop faible) | **Idem** : cerveau sur M5/M1, le robot est un corps | Architecture hôte + LLM local |
| Deux chemins cerveau : IA-HA native vs Dobby | **Cloud (GPT) vs local (Ollama M1)** | Partir **local** (cohérent avec la vision JC) |
| Latence 2–4 s (réseau → IA → audio) | Local Ollama = latence plus faible + privé | Mesurer `gemma3:12b` (réactif) vs `gemma3:27b` (vision) |
| Micro d'origine médiocre → entrée via téléphone/Atom Echo | Cozmo **n'a pas de micro** (haut-parleur seul) — contrairement à Vector (4 micros) | Entrée vocale via téléphone ou micro dédié (~15 €) |

---

## Architecture cible

```
Cozmo (caméra + moteurs + écran facial)
   │  WiFi 2,4 GHz (app Cozmo sur téléphone/tablette)
   ▼
M5 (Mac) — SDK Python `cozmo` + orchestration
   │  Tailscale
   ▼
M1 — Ollama : gemma3:27b (vision), gemma3:12b, qwen2.5-coder:32b
   │
Home Assistant (M5/RPi) — présence, automatisations, notifications
```

Vérifié en direct le 2026-11-09 : M1 Ollama répond (`100.73.212.110:11434`) avec `gemma3:27b` **vision**, HA M5 répond (`localhost:8123` HTTP 200).

---

## Étape 1 — PoC (preuve en ~1 session si le SDK passe)

1. **Recenser le matériel** : quel Cozmo (1.0 vs 2.0), état batterie, téléphone/tablette compatible disponible, état de l'app.
2. **Installer** l'app Cozmo + le SDK Python (`cozmo`) sur le M5, appairer le robot.
3. **Capturer** une image caméra → l'envoyer à `gemma3:27b` (vision) sur le M1 → récupérer une description.
4. **Faire parler** le Cozmo (TTS) avec une expression.

---

## Points à vérifier (verrous)

- [x] Modèle exact : **Cozmo Classic (Anki 1.0)** + batterie OK (recensé 2026-11-10)
- [x] App : **« Cozmo Robot » (Digital Dream Labs LLC)** — $2,99 paiement unique, iOS 12+, macOS 11+ (Apple Silicon, « not verified »). Fonctionne (oct 2025). ⚠️ Ne pas prendre « Cozmo 2.0 » (réservé au robot 2.0)
- [ ] SDK Python compatible (version Python requise, souvent ancienne)
- [ ] SSID 2,4 GHz disponible (ou réseau dédié RUT240)
- [ ] TTS : la voix du Cozmo est générée côté app — injectable en local ?
- [ ] Latence acceptable pour un compagnon « vivant »

## Décisions à trancher

- **Cerveau** : local Ollama (M1) vs cloud (GPT) → reco **local**.
- **Hôte SDK** : M5 (fixe) vs RPi → reco **M5** pour démarrer.
- **Entrée vocale** : micro dédié (Atom Echo ~15 €) vs téléphone.
- **Appareil appairé (app Cozmo)** : **iPad iOS 13** ✅ — app « Designed for iPad », iOS 12+ requis.

---

## Références

- `../karotz-reborn/resurrection-karotz-2026-11-09.md` — leçons complètes du revival.
- `../karotz-reborn/integration-home-assistant.md` — plomberie HA (pipeline Assist, TTS, media_player).
- SDK Cozmo : package PyPI `cozmo` + `cozmo-tools` (communauté) · app Cozmo/DDL.

---

*Fichier de travail Dobby 🦉 — à compléter après recensement du matériel et premier PoC. Une fois le revival fait, produire un postmortem type `resurrection-cozmo-YYYY-MM-DD.md` comme pour le Karotz.*