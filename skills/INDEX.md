# PKA Skills — Index transversal

**Emplacement canonique :** `PKA_JCH/skills/`  
**Dernière mise à jour :** 2026-05-25  
**Plateformes :** Claude Code (symlinks `~/.claude/skills/`), Gemini CLI, DeepSeek, Codex

## Utilisation

**Claude Code :** `Skill` tool → chargement automatique via symlinks.  
**Autres plateformes :** lire le `SKILL.md` correspondant et suivre les instructions exactement.

---

## Skills disponibles

| Skill | Trigger(s) | Description courte |
|-------|-----------|-------------------|
| [wildnexus-bom](wildnexus-bom/SKILL.md) | "génère le BOM", "mets à jour le budget", "shortlist achat" | Générer/mettre à jour le BOM WildNexus P0 en Excel multi-onglets |
| [wildnexus-adr](wildnexus-adr/SKILL.md) | "crée un ADR", "passe l'ADR en accepté", "documente la décision" | Créer, mettre à jour ou valider un ADR WildNexus |
| [onboarding-specialiste](onboarding-specialiste/SKILL.md) | "recrute", "gap de compétence", "nouvel agent", "embauche" | Pipeline complet recrutement d'un spécialiste PKA (10 étapes) |
| [pka-session-start](pka-session-start/SKILL.md) | Automatique — début de session | Protocole démarrage Dobby : modèle, mémoire, inbox, confirmation |
| [pka-file-versioning](pka-file-versioning/SKILL.md) | Automatique — avant toute modif significative BOM/ADR/registre | Sauvegarder la version précédente d'un fichier itératif |
| [pka-pointer-sync](pka-pointer-sync/SKILL.md) | "mets à jour les pointers", "l'équipe a changé" | Resynchroniser CLAUDE.md, AGENTS.md, GEMINI.md, DEEPSEEK.md |
| [bioacoustics-qc-playbook](bioacoustics-qc-playbook/SKILL.md) | "bioacoustics QC", "segment triage", "spectrogram review", "insect dataset" | Curation datasets bioacoustiques, QC spectrogrammes, profils espèces audio |
| [obsidian-knowledge-graph](obsidian-knowledge-graph/SKILL.md) | "wikilink le vault", "dry-run obsidian", "mets à jour le knowledge graph" | Inventaire Obsidian, dictionnaire, dry-run wikilinks et application contrôlée |

---

## Ajouter un skill

1. Créer `skills/<nom>/SKILL.md` avec frontmatter `name`, `description`, triggers
2. Ajouter la ligne dans ce tableau
3. Pour Claude Code : `ln -s /Users/jchavauxm5/PKA_JCH/skills/<nom> ~/.claude/skills/<nom>`
4. Les autres plateformes voient le skill automatiquement via ce fichier INDEX.md
