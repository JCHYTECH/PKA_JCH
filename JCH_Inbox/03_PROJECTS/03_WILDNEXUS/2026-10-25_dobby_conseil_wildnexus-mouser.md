# CONSEIL — VERDICT

> Skill `conseil` — dry-run. Mode : CONSEIL COMPLET (5 stances). Chairman : Dobby 🦉.
> Date : 2026-10-25. Domaine : WildNexus P0 (hardware). Seed : gouvernance Satellite-Lite + Scope Lock + hardware-state.

## Décision

Faut-il commander maintenant le panier Mouser restant WildNexus P0 (~279€, 11 composants BOM) alors que le projet est gelé jusqu'à post-van (post-15/12), ou reporter la commande à la reprise ?

## Les 5 stances

| Stance | Lecture | Avis |
|--------|---------|------|
| **Contrarian** | Donnée décisive : « bench loop non repris ». Design P0 figé sur papier, jamais validé au banc. Commander une BOM complète pour un design non validé = acheter des certitudes qu'on n'a pas. Cash en concurrence directe avec IOT/Vanlife (15/12). | **Attendre** |
| **Premiers Principes** | Cadrage faux : ce n'est pas « maintenant vs plus tard », c'est un problème de validité du BOM. WP02 gelé + « chaque capteur ajoute complexité » ⇒ BOM probablement périmé. Le hardware déjà reçu (PPK2, ESP32-S3, CAM) suffit à relancer le bench. | **Attendre** (pas de conditionnel) |
| **Expansionniste** | Les fenêtres lead-time/EOL ne respectent pas les gels. Références de niche (MEMS I2S, module LoRa, PMIC) : 8-12 semaines de lead-time. Une EOL pendant le gel bloquerait la replanification, et InsectNet + NEXUS_ACOUSTIC dépendent du P0. 279€ = assurance bon marché contre une rupture au redémarrage. | **Conditionnel** (verrouiller les refs à risque) |
| **Outsider** (zéro contexte) | La pause ≠ pas besoin d'acheter : c'est justement le seul moment où on absorbe un délai fournisseur sans bloquer personne. Variables absentes : lead-time, volatilité prix, pénurie, BOM gelé ? | **Conditionnel** : commander seulement si lead-time > temps restant + marge, sinon attendre |
| **Prémortem** | Avril 2026 : le projet n'a redémarré qu'en mars, le BOM a bougé, les 279€ sont devenus du stock mort. Coût d'attendre = quelques jours de délai ; coût de commander = 279€ de pièces potentiellement fausses. | **Attendre** |

## Verdict

**Recommandation : CONDITIONNEL — scinder le panier, ne pas commander les 279€ d'un bloc.**

- **Commander maintenant** : uniquement les références de niche à risque EOL / lead-time long (module LoRa, PMIC, MEMS I2S si la ref est stable) — la « prime d'assurance » de l'Expansionniste, mais réduite au sous-ensemble réellement exposé.
- **Reporter** : le reste (capteurs / chaîne analogique), à la reprise, après revalidation du BOM au bench.

**Arguments pour (commander maintenant)** : verrouille les refs à lead-time long avant une EOL ; 279€ est une assurance faible coût face à une rupture au redémarrage (qui bloquerait InsectNet + NEXUS_ACOUSTIC en cascade).

**Arguments contre (commander maintenant)** : BOM non validé au banc (bench loop non repris), WP02 gelé ⇒ forte probabilité que le BOM change ⇒ 279€ de stock mort ; cash en concurrence directe avec la deadline dure IOT/Vanlife du 15/12.

**Objection la plus forte** (à l'attente intégrale) — **Expansionniste** : reporter intégralement expose à une EOL/rupture sur les références de niche exactement au redémarrage, quand on n'a plus le temps de l'absorber.

**Réponse à l'objection** : le risque EOL est réel mais *ciblé* — il ne justifie que les références de niche, pas le panier entier. Le risque de validité du BOM (Contrarian + Prémortem) domine pour les capteurs/analogique, que Satellite-Lite tend à ajouter puis retirer. On réduit donc l'exposition de 279€ à une petite prime d'assurance sur les refs à risque.

**Résidu de risque** : si une référence reportée part en EOL pendant le gel, il faudra redesign à la reprise — mais c'est un redesign qu'on aurait de toute façon dû faire (WP02 gelé, design jamais validé au banc).

**Dissent** : Expansionniste maintient qu'un report intégral est plus risqué qu'une couverture partielle — objection intégrée dans la recommandation « scindée », pas écartée.

## Suivi — classification du panier (Forge + Bruno → synthèse Dobby)

Les 11 lignes du panier restant (source : `WILDNEXUS_stock.md`) :

| # | Composant | Verdict |
|---|-----------|---------|
| 1 | Module LoRa **RAK3172-T EU868 (SX1262)** ×2 | ✅ **Commander** — bloque SOP-07 ; comm LoRa verrouillée par Scope Lock, pas à risque de redesign. ⚠️ corrigé : `WILDNEXUS_stock.md` notait « RFM95W ×3 » (erroné/stale) — le BOM v0.4 (B02) + ADR-003 + fiches F1/S1/S2 spécifient tous RAK3172 (SX1262) |
| 10 | Carte microSD industrial 16GB ×3 (Swissbit S-45U pSLC) | ✅ **Commander** — single-source pSLC, lead-time/EOL réel |
| 4+9 | Connecteur u.FL/IPEX ×3 + connecteur microSD push-push ×3 | ✅ **Bundle** — standards mais co-requis des 2 ci-dessus (évite un 2e port Mouser) |
| 2 | Connectique (JST, headers, câbles) | ⏸ Reporter — standard, zéro risque |
| 3 | Passifs CMS R+C 0402/0603 | ⏸ Reporter — standard (lot 0603 déjà reçu) |
| 5 | Support CR2032 + pile ×3 | ⏸ Reporter — standard |
| 6 | Diode Schottky / TVS | ⏸ Reporter — standard |
| 7 | Quartz 32.768 kHz ×3 | ⏸ Reporter — commodity |
| 8 | Résistances shunt précision | ⏸ Reporter — standard |
| 11 | Divers (LED, boutons, jumpers) | ⏸ Reporter — standard |

**Split € recommandé :**
- **~110–120 € maintenant** : RFM95W (~50 €) + Swissbit S-45U (~54 €) + connecteurs u.FL/push-push (~10 €).
- **~160–170 € à la reprise** : le reste, après revalidation au bench.

**Logique** : on ne finance pas l'incertitude (les capteurs/analogique qui bougeront au bench), mais on verrouille les deux références qui (a) bloquent le banc ou (b) sont single-source à lead-time long. L'enveloppe de ~120 € ne déstabilise pas la trésorerie de la deadline 15/12 (Zigbee ~88 € + silentblocs + coating).
