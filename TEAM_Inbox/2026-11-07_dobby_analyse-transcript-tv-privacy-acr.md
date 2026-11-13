> Dobby 🦉 — DeepSeek — 2026-11-07

# Analyse transcript — « Voici ce que l'IA vient de trouver dans nos télés »

## Résumé

Essai vidéo YouTube (~26 min, anglais) sur la vie privée des TV connectées. Deux récits entrelacés :
1. **Log4j** — un chercheur root une Samsung 2025 (Tizen), publie ses découvertes (réseaux de neurones `logo_cnn` / `AlexTFLite`, compteurs d'aboiement/pleurs, service « Always On Voice », 400 partenaires), et son compte OpenAI est banni.
2. **Clean Your TV** — un dev utilise **Claude Code** avec le n° de modèle d'une TV Xiaomi → l'agent désactive 25 packages et écrit un launcher custom. 50k+ étoiles GitHub.

Thèse : l'affaire « Samsung espionne » est largement sur-interprétée, mais elle révèle un basculement réel — **l'IA (agents + modèles locaux) rend l'inspection et la reprise de contrôle d'un appareil accessibles à tous**.

## Confirmation (fact-check)

- ✅ **Établi** : Samsung a annoncé *Pet Care / Family Care* (avril 2025) → les compteurs ne sont pas une découverte cachée. Vizio condamné 2017 (11 M foyers, 2,2 M$, 20 ¢/foyer). Walmart a acheté Vizio 2,3 Md$ (2024). Texas AG a poursuivi 5 constructeurs. GDPR art. 7 + CNIL.
- ⚠️ **Affirmé, à confirmer** : détail des modèles CNN ; serveur Vidaa sans mot de passe (57 M reconnaissances) ; motif réel du bannissement OpenAI.
- ❓ **Non prouvé (reconnu par la source)** : aucun lien bruits → pubs ; « Always On Voice » = simple nom de service ; les études se contredisent sur la coupure réelle de l'ACR après désactivation.

## Impact croisé

- 🔴 **01_AI_IT_TOOLS** — pattern « agent IA + n° de modèle → inspecte/débloate » (template réutilisable).
- 🟡 **11_IOT / Vanlife** — question TV dans Lupo → **tranchée : pas de TV** (voir Décision).
- 🟢 **NEXUS_ACOUSTIC + WILDNEXUS_DEVICE** — CNN audio on-device = benchmarks TinyML (pointers posés).

## Actions

- ✅ Décision enregistrée : pas de TV dans Lupo.
- ✅ Bookmark veille : Clean Your TV + Glasshouse.
- ✅ Pointers posés pour NEXUS_ACOUSTIC + WILDNEXUS_DEVICE.
- ⚪ **P2 à venir** : benchmark nos modèles edge vs CNN embarqués (post-van).

## Décision

**Pas de TV connectée dans Lupo** — cohérent avec local-first (HA local, Mosquitto local). Si écran nécessaire : box HDMI + TV déconnectée d'Internet.

## Routing

Source déplacée : `01_AI_IT_TOOLS/99_REFERENCES/tv-privacy-acr_2026-11-07/`
Indexée dans `file_index` · 6 connaissances capturées (`knowledge`) · 2 bookmarks · décision dans `decisions-actives.md`.
