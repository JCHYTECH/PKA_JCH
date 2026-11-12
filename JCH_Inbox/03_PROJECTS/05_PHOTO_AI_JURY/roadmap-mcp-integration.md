# Roadmap — Intégration MCP dans le pipeline [[Argus]]

> Créé le 2026-06-16 par [[Dobby]] 🦉
> Contexte : découverte de lightroom-mcp et photoshop-mcp comme ponts IA ↔ Adobe

## Pipeline actuel

```
Photo → Claude (analyse) → Scores (/20) + lr_params (JSON)
                                  ↓
                           PDF rapport + XMP sidecar
                                  ↓
                           JCH applique manuellement dans LR
```

**Problème** : `lr_params` est généré mais jamais appliqué automatiquement.
La DB `argus_critique.db` contient déjà un champ `lr_params TEXT` (JSON) prévu pour ça.

## Pipeline cible — Phase 1 (Lightroom)

```
Photo → Claude (analyse) → Scores + lr_params (JSON)
                                  ↓
                           lightroom-mcp → Lightroom Classic
                                  ↓
                           Réglages Develop appliqués automatiquement
                           + Export JPEG/TIFF
                           + Classement collection (par tier/espèce)
```

Cette cible n'autorise ni application automatique ni traitement en lot sans validation humaine préalable. Le module local `mcp_apply_lr.py` prépare seulement les paramètres SDK ; le test technique MCP et le jugement artistique JCH sont deux étapes distinctes.

**Outil** : `github.com/Automaat/lightroom-mcp` (MIT, v0.4.1, 29⭐)
- Plugin Lua dans LR Classic + serveur MCP Node
- Communication TCP localhost, token 256-bit
- Fonctionne avec Claude Desktop, Claude Code, Codex CLI

**Ce qu'il permet** :
- `set_develop_settings` → appliquer le JSON `lr_params` directement
- `search_photos` → filtrer par note, espèce, date
- `apply_develop_preset` → appliquer des presets
- `export_photos` → export automatisé
- `manage_collections` → créer/mettre à jour des collections par tier

## Pipeline cible — Phase 2 (Photoshop)

Pour les retouches avancées (détourage, nettoyage, compositing) :

**Outil** : `github.com/alisaitteke/photoshop-mcp` (MIT, 106⭐)
- 50+ outils : calques, filtres, sélections, texte, export
- AppleScript (macOS) + ExtendScript

## Prérequis techniques

- Lightroom Classic installé sur M5 (déjà fait)
- Node.js 22+ (déjà fait)
- Plugin Lua à installer dans `~/Library/Application Support/Adobe/Lightroom/Modules/`
- Serveur MCP à configurer dans `~/.deepseek/config.toml` ou équivalent

## Prochaines étapes

1. [x] Installer le plugin lightroom-mcp dans Lightroom Classic
2. [x] Ajouter le module `mcp_apply_lr.py` dans le projet [[Argus]]
3. [x] **Geste manuel JC effectué** : Lightroom Classic et **Start Server** actifs ; JC a confirmé que la RAW sélectionnée `Evieux-42.CR3` est une copie virtuelle.
4. [x] Exécuter `_local/lightroom-mcp/tests/e2e/mcp-runner.mjs` en mode `read` : **8/8 contrôles réussis**, exactement une RAW sélectionnée. Les modes `develop`, `write`, `all`, les presets et la copie entre photos n'ont pas été lancés.
5. [x] Avec l'accord de JC, le mode borné `exposure-restore --virtual-copy-confirmed` a lu la baseline `0`, testé uniquement `Exposure2012 +0,10`, relu `0,10`, puis restauré et revérifié `0` dans un `finally`. Une lecture indépendante a confirmé la restauration.
6. [ ] Faire juger les propositions A/B par JCH, avec explication tutoriel ; confronter le résultat à une image inédite avant toute application ou lot automatique.
7. [ ] Phase 2 ultérieure : intégration photoshop-mcp pour retouches, après validation du socle Lightroom.

### État au 2026-11-06

Le test technique Lightroom est **réussi** sur la copie virtuelle RAW explicitement confirmée par JC : ports locaux actifs, 8/8 lectures, exposition `0 → +0,10 → 0` et restauration confirmée par une lecture indépendante. Aucune autre retouche, aucun preset et aucun traitement par lot n'ont été appliqués. La validation artistique A/B et le test sur image inédite restent à faire.

Le socle `jch_feedback.py` a été testé deux fois sur une copie SQLite, puis appliqué à la base canonique. Le schéma v1 conserve 52 analyses et 16 évaluations de rapports ; les trois tables de sessions, propositions et validations de retouche sont vides. Les votes sur les rapports ne sont pas transformés en préférences de style : il n'existe encore **aucun dataset artistique JCH**.

### Setup effectué le 2026-06-16

| Composant | État |
|-----------|------|
| Node.js v25.9.0 | ✅ |
| Lightroom Classic | ✅ installé |
| Plugin Lua (LightroomMCP.lrplugin) | ✅ dans `~/Library/Application Support/Adobe/Lightroom/Modules/` |
| Serveur MCP (v0.4.1) | ✅ dans `_local/lightroom-mcp/` |
| Config Codex | ✅ `~/.deepseek/config.toml` → `[[mcp_servers]]` lightroom |
| Module [[Argus]] `mcp_apply_lr.py` | ✅ mapping 51 clés SDK, commandes `prepare`/`map`/`sdk-keys` |
| Activation plugin ([[Start]] Server) | ✅ Activation manuelle effectuée et testée le 2026-11-06 |
