# Analyse transcript — DeepSeek Harness « Creator Mode »

> Dobby 🦉 — 2026-11-08 — Projet 01_AI_IT_TOOLS
> Source : `NoteGPT_Transcript_DeepSeek Harness Creator Mode Is Actually INSANE!.txt` (YouTube, EN)

## Nature

Vidéo EN (~8,5 min), avatar de Julian Goldie (agence AI SEO/GEO). Mix promo + démo réelle de DeepSeek Harness.

## Thèse

DeepSeek Harness (framework open-source « agent = modèle + harness », bâti sur Cordis, MIT) introduit un « creator mode » : l'agent construit lui-même ses propres plugins / features à partir d'une phrase.

## Points clés

- Harness ≠ modèle : le modèle pense, le harness donne mains / fichiers / terminal / recherche / skills / tâches planifiées / écran.
- Tout est plugin (connexion modèle, outils, boucle agent, UI) → interchangeable ; non verrouillé à DeepSeek (endpoints OpenAI-compatibles).
- 4 modes : Standard, Code, Minimal, Creator. Creator = Standard + outils pour inspecter / tester / écrire des plugins + presets.
- Démo officielle : « write a Pomodoro timer plugin for me » → plugin écrit, installé, vérifié en 5 min 24 s.
- 7 prompts officiels (3D gallery, transformer visualizer, theme switcher, poster workbench, video editor, paper reader, stats).
- Pattern des prompts : (1) dire où ça vit (sidebar), (2) nommer les éléments indispensables, (3) dire ce qu'on ne veut pas, (4) s'attendre à plusieurs tours.
- Install : `npx @deepseek-ai/dsh web` ou app desktop (Mac Apple Silicon / Windows).

## Confirmer

- ✅ **Établi** : DeepSeek Harness existe (repo GitHub, licence MIT, preview publique) ; « agent = modèle + harness » ; framework Cordis.
- ⚠️ **Affirmé (auteur)** : démo « 5 min 24 s », les 7 prompts exacts, ~269k stars GitHub au 2 nov.
- ❓ **Non prouvé** : chiffre exact des stars ; la « fenêtre » business invoquée.

## Conseiller — ⚠️ sécurité

- La source elle-même met en garde : **preview dev, pas d'audit sécurité, breaking changes attendues, un plugin = vrai code** (accès fichiers / réseau / credentials). Pratiques : dossier de test, examiner un plugin tiers avant ajout, garder les prompts d'approbation.
- **Routing** : `01_AI_IT_TOOLS/99_REFERENCES/deepseek-harness-creator_2026-11-08/`.
- **Impact croisé** : 🔴 AI_IT_TOOLS (on tourne sur DeepSeek — ce TUI ; creator mode = même logique que nos skills) ; 🟡 Forge (code) et Dobby (orchestration / sub-agents).
- **Action proposée** : ✅ testé en sandbox le 08/11 (agent headless + clé DeepSeek → plugin `pomodoro.html` généré et vérifié, ~13,6 Ko). **Verdict** : P2 veille — pas un remplaçant de nos `skills/` + sub-agents, mais le « self-extending UI » est intéressant ; re-tester dans 1-2 versions.
