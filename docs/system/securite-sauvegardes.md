# Sécurité & Sauvegardes — PKA_JCH

> Dobby 🦉 — 2026-07-16
> À relire annuellement ou après tout changement de machine.

---

## Niveaux de confidentialité

| Niveau | Dossier | Contenu | Accès |
|--------|---------|---------|-------|
| 🔴 Privé | `JCH_PRIVATE/` | Mots de passe, tokens, contrats, docs personnels | JC uniquement |
| 🟡 Interne | `JCH_Inbox/`, `TEAM/` | Projets, analyses, mémoire agents | JC + agents PKA |
| 🟢 Public | `wiki/`, `PHOTO/`, `graphify-out/` | Connaissances, photos, graphe | Tout agent |

**Règle** : aucun secret (token, password, clé API) ne doit apparaître dans un fichier hors `JCH_PRIVATE/`. Si un agent génère du code avec des secrets, il doit les remplacer par `$ENV_VAR` et stocker la valeur dans `JCH_PRIVATE/credentials-central.md`.

---

## Sauvegardes

| Quoi | Où | Fréquence | Méthode |
|------|----|-----------|---------|
| Vault PKA_JCH complet | iCloud Drive (automatique) | Continue | Synchronisation iCloud |
| `TEAM/team.db` | `TEAM/backups/` | Avant chaque migration | `mcp_pka--sqlite` export |
| Fichiers critiques | `_local/state/`, `.git/` | À chaque commit | Git |

**Restauration** : `TEAM/RESTORE_TEAM_DB.md` pour team.db. Pour le reste, iCloud ou Git.

---

## Règles agent

1. **Ne jamais exposer de secrets** dans les logs, les commits, ou les réponses visibles
2. **Toute opération destructive** (`rm -rf`, `DROP TABLE`, `force push`) nécessite confirmation explicite de JC
3. **Les tokens d'API** sont stockés dans `JCH_PRIVATE/credentials-central.md` et référencés par variable d'environnement
4. **Vérifier l'identité** avant d'exécuter des commandes sur des machines distantes (hostname, IP)
