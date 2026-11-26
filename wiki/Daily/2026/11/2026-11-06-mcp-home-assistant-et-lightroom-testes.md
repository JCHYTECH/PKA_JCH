---
date: 2026-11-06
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-06 — MCP Home Assistant et Lightroom testes

## Session — 14:08 — MCP Home Assistant et Lightroom testes

### Contexte
- Modèle : kimi-code
- Projet : PHOTO_AI_JURY

### Résumé
Trois transcripts YouTube convertis en chantier concret : MCP Home Assistant Lupo en lecture seule testé avec Kimi et DeepSeek, supervision AirGuard et premier instantané Time Machine vérifiés ; socle SQLite de retour JCH migré sans perte et test MCP Lightroom réversible réussi avec restauration confirmée.

### Actions
- Relais local persistant et filtres MCP Home Assistant read-only vérifiés ; appels capteurs réels réussis dans Kimi et DeepSeek.
- Dashboard AirGuard validé ; Time Machine configuré à 03:17 avec première copie de 10 fichiers et 52 KiB, puis diff Lovelace. Aucune restauration effectuée.
- Base Argus migrée au schéma v1 après sauvegarde : 52 analyses et 16 évaluations conservées, intégrité et clés étrangères validées ; trois tables de retour JCH créées vides.
- Lightroom MCP : 8 tests read sur 8 réussis ; sur copie virtuelle RAW confirmée par JC, exposition 0 vers +0,10 puis restauration 0 dans finally et nouvelle lecture indépendante.
- Documentation projet et graphify actualisés ; aucun appel IA payant ni traitement photo par lot.

### Décisions
- Aucun accès Home Assistant public ni outil domotique d’action ; sécurité incendie, CO et sécurité locale déterministe.
- Time Machine reste un instantané de configuration Lovelace, pas une sauvegarde complète HA.
- Les votes sur les rapports Argus ne deviennent pas un dataset de style ; validation artistique JCH distincte du succès technique MCP.
- Tests Lightroom uniquement sur copie virtuelle RAW explicitement confirmée, avec restauration exacte de la baseline.

### Prochaines étapes
- Traiter physiquement l’alerte Under-voltage detected du Raspberry Pi.
- Vérifier la prochaine exécution automatique Time Machine après 03:17, prévoir une copie hors du RPi et ne tester une restauration qu’avec accord explicite.
- Reconnecter Claude et résoudre séparément les modèles Codex refusés ; ChatGPT Web et MCP M5 restent non validés.
- Recueillir les choix A/B de JCH avec tutoriel et validation sur image inédite avant toute généralisation ou application par lot.
