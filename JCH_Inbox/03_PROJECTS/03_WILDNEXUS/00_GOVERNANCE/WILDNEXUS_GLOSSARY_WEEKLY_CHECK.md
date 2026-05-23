# WildNexus — Routine hebdomadaire de check glossaire

**Version :** v0.1  
**Date :** 2026-05-18  
**Statut :** actif — phase 1 manuelle  
**Owner principal :** Atlas  
**Reviewers :** Corbeau + Dobby  
**Support automation :** Forge  
**Fréquence cible :** hebdomadaire, idéalement lundi  

## 1. Objet

Maintenir [../01_FOUNDATION/WILDNEXUS_GLOSSAIRE.md](../01_FOUNDATION/WILDNEXUS_GLOSSAIRE.md) comme document d'onboarding humain.

Le glossaire doit expliquer les termes que les nouveaux entrants risquent de rencontrer dans WildNexus : acronymes, codes projet, jalons, composants, standards, termes juridiques, termes terrain et termes IA.

## 2. Décision d'automatisation

La routine démarre **sans cron** et sans `launchd`.

Progression retenue :

| Phase | Mode | Statut |
|---|---|---|
| Phase 1 | Checklist manuelle hebdomadaire | Active |
| Phase 2 | Script de scan lançable à la demande | À envisager après 2-3 cycles |
| Phase 3 | Automatisation hebdomadaire `launchd` | Seulement si le script prouve son utilité |

Raison : éviter les rapports automatiques bruyants tant que le vocabulaire et le rythme documentaire ne sont pas stabilisés.

## 3. Responsabilités

| Rôle | Responsable | Mission |
|---|---|---|
| Owner glossaire | Atlas | Proposer les ajouts, reformuler pour humains non spécialistes, garder la structure lisible |
| Qualité connaissance | Corbeau | Détecter doublons, incohérences, termes ambigus ou définitions contradictoires |
| Validation | Dobby | Arbitrer ce qui entre dans le glossaire, éviter l'inflation inutile |
| Automatisation future | Forge | Créer un script de scan seulement si la phase 1 montre un besoin réel |

## 4. Sources à vérifier chaque semaine

Priorité haute :

- `01_FOUNDATION/*.md`
- `02_DECISIONS/**/*.md`
- `03_P0_ENGINEERING/*.md`
- `00_GOVERNANCE/*.md`

Priorité moyenne :

- `04_PRINT_EXPORTS/*.md`
- `05_VISUALS_DASHBOARDS/*.md`
- `06_COMPONENTS/**/*.md`
- `07_AGENTS/**/*.md`
- `08_TECH_NOTES/**/*.md`

## 5. Checklist hebdomadaire

1. Lire les fichiers modifiés depuis le dernier check.
2. Identifier les nouveaux acronymes ou codes projet.
3. Identifier les termes techniques répétés au moins deux fois.
4. Vérifier si ces termes existent déjà dans le glossaire.
5. Ajouter uniquement les termes utiles à un humain entrant dans le projet.
6. Supprimer ou fusionner les définitions redondantes.
7. Mettre à jour la date et la version du glossaire si modification réelle.
8. Noter le passage dans la section "Journal de check" ci-dessous.

## 6. Critères d'entrée dans le glossaire

Un terme entre dans le glossaire s'il répond à au moins un de ces critères :

- il apparaît dans une ADR, un jalon, un budget, un registre supply ou un document fondateur ;
- il est nécessaire pour comprendre P0/P1/P2 ;
- il est ambigu pour un non-spécialiste ;
- il a une signification spécifique à WildNexus ;
- il est utilisé comme code de pilotage (`ADR`, `M-01`, `T01.3`, `NN-05`, etc.).

Un terme ne doit pas entrer s'il est :

- trop générique ;
- utilisé une seule fois sans impact ;
- évident pour le public cible ;
- mieux traité dans une fiche technique ou une ADR.

## 7. Commande manuelle utile

Pour repérer rapidement les acronymes et codes probables :

```bash
rg -n "\\b[A-Z][A-Z0-9-]{2,}\\b|\\b[A-Z]{1,3}-[0-9]{2}\\b|\\bT[0-9]{2}\\.[0-9]\\b|\\bD[0-9]{2}\\.[0-9]\\b" JCH_Inbox/03_PROJECTS/03_WILDNEXUS --glob '*.md'
```

Cette commande est indicative. Atlas décide ensuite ce qui mérite vraiment d'entrer dans le glossaire.

## 8. Journal de check

| Date | Responsable | Résultat | Action |
|---|---|---|---|
| 2026-05-18 | Dobby | Routine créée ; phase 1 manuelle retenue | Prochain check hebdomadaire à lancer après nouvelles ADR ou nouveaux livrables |
