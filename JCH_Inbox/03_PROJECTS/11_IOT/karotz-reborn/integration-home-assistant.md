# Intégration Home Assistant — Karotz Reborn

> Feuille de route complète pour transformer le Karotz en assistant IA piloté par Home Assistant.
> **Source** : Google Gemini (copié-collé par JC 2026-11-08) + communauté Home Assistant. ⚠️ À **vérifier** lors de la mise en œuvre (références GitHub exactes, compatibilité HACS, endpoints).

---

## Architecture

- **Karotz** = l'interface (corps, voix, détection, oreilles, LED, RFID).
- **Cerveau** = déporté (M5/HA + IA) — le lapin d'origine est trop faible pour ça.
- **Home Assistant** = la plomberie (pipeline de conversation, TTS, media_player, automatisations).

---

## Étape 1 — Libérer le Karotz (OpenKarotz)

- Clé USB FAT32 + flash **OpenKarotz** (miniil Karotz OS).
- Le lapin s'installe seul en quelques minutes.
- Interface Web accessible à son IP locale.

*(détail de la procédure : voir le README et le guide miniil.be)*

---

## Étape 2 — Connecter à Home Assistant (2 options)

1. **Intégration native OpenKarotz** (dans HA : « Media Player » + boutons).
2. **Script communautaire « Karotz 2025/2026 »** — `Desperado88/Home-Assistant-Karotz-2025` (GitHub, via HACS). Gestion plus fine, notamment la **synchronisation des oreilles avec les phrases lues**.

À trancher : natif (simple) vs script HACS (plus fin). Le script HACS est recommandé par Gemini pour les oreilles.

---

## Étape 3 — Le cerveau IA (2 chemins — à trancher)

| | IA-HA native | Dobby (vision JC) |
|---|---|---|
| Cerveau | OpenAI Conversation / Google Generative AI / Anthropic (intégration HA) | Dobby — DeepSeek V4 sur M5 |
| Personnalité | prompt système « Tu es un lapin nommé Karotz… » | Dobby lui-même (SOUL.md) |
| Simplicité | haute (clé API + prompt) | moyenne (passerelle Dobby→HA en écriture) |
| Dépendance | clé API tierce | aucune (M5 local) |

- **IA-HA** : Paramètres → Appareils et services → Ajouter → OpenAI Conversation (ou Google/Anthropic) → clé API → System Prompt.
- **Dobby** : Dobby génère le texte → HA TTS → `media_player.karotz`. Nécessite une passerelle Dobby→HA en **écriture** (le relais MCP actuel est **lecture seule**).

---

## Étape 4 — Flux de conversation (Assist)

1. Créer un **pipeline de conversation** (protocole Assist) utilisant l'IA.
2. **Entrée vocale** : app Home Assistant sur téléphone, OU micro satellite **Atom Echo ~15 €** posé à côté du lapin — car le **micro d'origine du Karotz est médiocre**.
3. **Sortie audio** : le pipeline envoie la réponse générée vers `media_player.karotz` → le lapin **prononce** la réponse avec sa vraie voix.

---

## Automatisations à tester

- **Badge magique** : badge RFID passé sous le nez → automatisation → l'IA génère une blague / un résumé météo, les oreilles tournent, il la raconte.
- **Gardien de la maison** : anomalie détectée (porte de garage restée ouverte) → HA demande à l'IA une alerte personnalisée → le Karotz **s'allume en rouge** pour la dire.

---

## Limites techniques (à garder en tête)

- **Micro d'origine médiocre** : reconnaissance vocale capricieuse en environnement bruyant → entrée via téléphone ou enceinte dédiée ; le Karotz sert de « porte-parole ».
- **Latence 2–4 s** : traitement local → internet (IA) → fichier audio → le lapin commence à parler.

---

## Références

- `Desperado88/Home-Assistant-Karotz-2025` (GitHub)
- Intégration HA `openai_conversation` (home-assistant.io/integrations/openai_conversation)
- Forum HA : « ChatGPT integration for Home Assistant » (community.home-assistant.io)
- freerabbits.nl/support
