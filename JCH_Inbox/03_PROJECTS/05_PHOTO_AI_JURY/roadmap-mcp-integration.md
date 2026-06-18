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
3. [ ] Lancer Lightroom Classic → Plug-in Manager → Lightroom MCP → [[Start]] Server
4. [ ] Tester `set_develop_settings` avec un `lr_params` réel d'[[Argus]]
5. [ ] Pipeline complet : photo → analyse → application LR automatique → export
6. [ ] Phase 2 : intégration photoshop-mcp pour retouches

### Setup effectué le 2026-06-16

| Composant | État |
|-----------|------|
| Node.js v25.9.0 | ✅ |
| Lightroom Classic | ✅ installé |
| Plugin Lua (LightroomMCP.lrplugin) | ✅ dans `~/Library/Application Support/Adobe/Lightroom/Modules/` |
| Serveur MCP (v0.4.1) | ✅ dans `_local/lightroom-mcp/` |
| Config Codex | ✅ `~/.deepseek/config.toml` → `[[mcp_servers]]` lightroom |
| Module [[Argus]] `mcp_apply_lr.py` | ✅ mapping 51 clés SDK, commandes `prepare`/`map`/`sdk-keys` |
| Activation plugin ([[Start]] Server) | ⚠️ À faire dans Lightroom → Plug-in Manager |
