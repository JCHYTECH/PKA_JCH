# SOP-10 — Phase J : Alimentation AA + buck TPS62840

**SOP :** SOP-10
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel
**Statut :** ⛔ SUSPENDUE — ne pas exécuter avant validation des gates électriques
**Révision :** 2.0 — 2026-11-05
**Prérequis :** SOP-05 réussi, schéma exact du DevKit et du breakout TPS62840 disponibles
**Owner :** [[Forge]] + [[Bruno]]

---

## 1. Pourquoi la procédure est suspendue

La version 1.1 contenait deux instructions incompatibles avec le matériel :

- **6×AA en série (~9 V nominal)** vers un TPS62840 dont la plage recommandée s'arrête à **6,5 V** ;
- injection de **3,3 V sur la broche 5 V** du DevKit.

Ces instructions sont retirées. Toute mesure réalisée avec ce câblage doit être écartée jusqu'à vérification du montage et des données.

La présente version définit les gates de reprise. Elle n'autorise pas un essai tant que les cases du §3 ne sont pas validées avec des références de schéma et des mesures consignées.

## 2. Règles de sécurité non négociables

1. **Ne jamais connecter 6 AA en série au TPS62840.**
2. **Ne pas connecter le pack 4S2P L91** tant que sa tension maximale avec piles neuves, tolérances et froid n'est pas démontrée ≤6,5 V dans tous les cas.
3. **Ne jamais injecter 3,3 V dans une broche 5 V.** Le point d'injection 3,3 V ne peut être utilisé qu'après vérification du schéma exact de la carte et des risques de backfeed.
4. Sortie d'alimentation OFF avant chaque modification ; vérifier polarité et continuité avant mise sous tension.
5. Ne jamais alimenter simultanément le DevKit par USB et par une source externe non conçue pour cette configuration.
6. Le câblage Ampère Meter ou Source Meter du PPK2 doit suivre le manuel Nordic officiel ; aucun schéma historique non validé ne fait autorité.
7. Le firmware SOP-05 avec des délais simulés ne remplace pas les charges caméra, SD, IR, I2S et LoRa réelles pour le calcul d'autonomie final.

## 3. Gates de reprise

- [ ] Référence précise du breakout TPS62840 et schéma du feedback 3,3 V consignés.
- [ ] Référence précise du DevKit et schéma du point d'injection consignés.
- [ ] Première alimentation du régulateur prévue avec une source de banc limitée, réglée à une tension connue ≤6,5 V ; aucune source 6S AA.
- [ ] Tension maximale du pack 4S2P documentée par fiche fabricant et mesure ; marge écrite dans ADR-005.
- [ ] Câblage PPK2 validé par [[Forge]] d'après la documentation Nordic.
- [ ] Points d'arrêt définis : surtension, échauffement, comportement anormal ou dépassement des limites du montage.
- [ ] `progress.md` conserve SOP-10 à « blocked » tant qu'un gate reste ouvert.

Si la compatibilité 4S2P L91 n'est pas démontrée, arrêter et réviser la topologie du pack ou le régulateur dans ADR-005. Ne pas contourner cette décision par un essai direct.

## 4. Matériel de banc autorisé après levée des gates

| Élément | Exigence |
|---|---|
| Source de banc | Tension réglable ≤6,5 V, limitation de courant réglée selon le montage validé |
| Buck TPS62840 | Breakout identifié, sortie configurée à 3,3 V |
| Multimètre | Vérification hors charge puis en charge |
| PPK2 | Mode et câblage validés selon le manuel Nordic |
| Charge | DevKit ou module dont le point d'injection 3,3 V est validé |
| Pack 8×AA 4S2P | Introduit seulement après réussite des essais sur source de banc et gate de tension maximale |

## 5. Séquence de validation après réouverture formelle

### 5.1 Régulateur seul

1. Source OFF ; réaliser le câblage validé.
2. Vérifier la tension d'entrée avant le régulateur : elle doit rester dans la plage documentée.
3. Mesurer la sortie sans charge. Cible : **3,3 V ± 0,1 V**.
4. Si sortie absente, >3,6 V ou instable : couper et corriger le montage. Ne pas brancher le MCU.
5. Appliquer la charge de banc prévue et relever la régulation et le rendement à plusieurs niveaux représentatifs.

### 5.2 MCU et périphériques réels

1. Vérifier une seconde fois le point d'injection et l'absence d'alimentation concurrente.
2. Exécuter les profils SOP-04/05, puis les vraies charges caméra, IA, SD, IR, I2S et LoRa.
3. Relever tension minimale/maximale, courant de veille, pics et énergie par état côté batterie lorsque possible.
4. Mesurer séparément les cycles 96 FFT/jour et 24 clips/jour pour WP03/SOP-18.
5. Consigner les fichiers PPK2 bruts, la température, la configuration et la version firmware.

### 5.3 Pack AA

1. Mesurer la tension du pack neuf sans connexion au régulateur et la comparer au gate ADR-005.
2. N'autoriser la connexion que si la marge est documentée et acceptée.
3. Répéter les mesures de régulation et d'énergie avec la chimie retenue.
4. Calculer l'autonomie selon WP03 en Wh côté batterie ; ne pas mélanger les mAh du pack et du rail 3,3 V.

## 6. Enregistrements obligatoires

| Mesure | Valeur | Fichier/preuve |
|---|---|---|
| Tension maximale pack neuf | _____ | _____ |
| Tension d'entrée utilisée au banc | _____ | _____ |
| Tension buck hors charge | _____ | _____ |
| Tension minimale sous pic combiné | _____ | _____ |
| Courant deep sleep carte complète | _____ | _____ |
| Énergie événement jour / nuit | _____ | _____ |
| Énergie FFT / clip WAV | _____ | _____ |
| Rendement par niveau de charge | _____ | _____ |
| Stabilité sur 100 cycles | _____ | _____ |

## 7. Grille de décision

| Critère | GO | ORANGE | NO-GO |
|---|---|---|---|
| Gates électriques | Tous documentés et fermés | — | Un gate ouvert |
| Tension buck en charge | 3,3 V ±3 % | Écart expliqué sans dépassement composant | >3,6 V, instabilité ou reset |
| Deep sleep carte complète | <100 µA | 100–200 µA avec cause et correction | >200 µA |
| Énergie par événement | <1,5 mAh équivalent batterie | 1,5–2,5 mAh | >2,5 mAh |
| Budget complet WP03 | Tous cycles inclus | — | Audio, IR, retries ou pertes absents |

**Clôture :** SOP-10 ne peut être marquée « done » que si les mesures et les preuves du §6 sont rattachées dans `progress.md`, et si WP03 confirme que le budget complet est exploitable.

---

*Version 2.0 du 2026-11-05 — suppression des instructions 6S AA et d'injection sur broche 5 V, ajout de gates de reprise et des charges réelles nécessaires à WP03.*
