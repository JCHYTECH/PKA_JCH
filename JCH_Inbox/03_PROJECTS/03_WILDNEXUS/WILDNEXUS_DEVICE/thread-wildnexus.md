# Thread — WILDNEXUS_DEVICE

Dernière mise à jour : 2026-11-22. Fil de reprise maintenu par Dobby ; il ne remplace pas les preuves consignées dans `progress.md`.

## État en bref

Projet repris le 2026-11-11 (P0 engineering, décision JCH) ; dégel confirmé au pilotage le 2026-11-12. Les gates de reprise restent à lever avant tout montage : inventaire, factures, micros/PIR, matrice GPIO.

P0 vise un nœud ESP32-S3 avec caméra, PIR, deux micros, stockage microSD, filtre animal/non-animal et alertes LoRa. L'audio est capturé par minuterie, indépendamment du déclenchement image. Une gateway minimale de développement est requise pour prouver la réception LoRa ; la STATION commerciale reste une vision P1.

Seize ADR sont rédigés : 13 acceptés, ADR-010 accepté sous réserve, ADR-006 et ADR-011 proposés. ADR-015 n'est pas rédigé ; ADR-018 reste à produire.

## Preuves et limites

| Axe | État établi | Reste à prouver |
|---|---|---|
| Architecture | Scope P0 et contrats d'interface documentés | Références physiques, schémas et arbitrages restants |
| Firmware | 37/37 tests hôte historiques consignés en juillet | Exécution et intégration sur ESP32-S3 ; aucune équivalence matérielle acquise |
| Énergie | Phases A→C et cinq acquisitions PPK2 consignées ; modèle Wh créé | Phases D/E, cycle complet, froid et scénario 60 jours |
| Caméra et IA | Matériel caméra identifié ; procédure de benchmark à appliquer | Captures réelles, dataset, choix du modèle, rappel humain et animal |
| Audio | Contrat stéréo 16 kHz/16 bits, WAV + JSON et codec spectral sur hôte | Interface des micros TDK, fichiers réels et compatibilité des pipelines |
| Radio | Contrat binaire 48 octets, downlink 16 octets | Matériel non commandé ; transmission, gateway, portée, duty cycle et retries |
| Boîtier | Cible IP67 documentée, ADR-006 proposé | Choix, montage, optique nocturne et essais d'étanchéité |
| Budget | Projection provisoire ≈904 €, réserve théorique ≈96 € | Réconciliation des factures, HT/TTC, reliquat et autorisation de dépense |

Le dépassement du seuil interne de 900 € impose une pause des achats. L'engagé historique d'environ 610 € et les lignes visibles ne sont pas encore un total comptable certifié.

## Sécurité avant reprise

SOP-10 est suspendue. Ne pas assembler le pack 4S2P L91, ne pas appliquer 3,3 V sur la broche 5 V et ne pas suivre les anciens schémas d'alimentation avant validation ADR-005, vérification des datasheets et revue du câblage complet.

Les références des micros et du PIR doivent être relevées sur le matériel réel. Les exemples de GPIO dans les ADR et le processus de montage ne sont pas un pinout validé.

## TTD — Pending

### Ordre de reprise proposé

**Go JCH donné le 2026-11-11 (P0 engineering).** Aucun montage ni achat tant que les gates de reprise ne sont pas levés (inventaire, micros/PIR, schéma, matrice GPIO).

- [ ] Au `go` de JCH, inventorier le matériel et rapprocher factures, commandes et budget ; synchroniser Plane/kanban sans reprendre les anciennes échéances.
- [ ] Lever les points de sécurité électrique et confirmer micros, PIR et optique IR avant alimentation ou soudure.
- [ ] Reprendre les phases D/E, SOP-06, CAM-01/02, SOP-08/09 sur le matériel identifié.
- [ ] Exécuter SOP-13 puis SOP-14/15/17/18 ; tester les fichiers réellement produits dans les pipelines.
- [ ] Comparer les modèles d'IA avec CAM-03/SOP-11, y compris rappel humain, fausses alertes animales, RAM, latence et énergie.
- [ ] Après arbitrage d'achat, exécuter SOP-07 et livrer la gateway P0 : réception des deux types de paquets, journal et erreurs.
- [ ] Mesurer le système intégré en Wh, puis décider du boîtier et de l'EVT. Ne pas annoncer 60 jours, une portée ou IP67 avant mesure.
- [ ] Rédiger ADR-018 et finaliser les exigences RGPD/sécurité avant le terrain.

## Décisions récentes

| Date | Décision |
|---|---|
| 2026-11-12 | Dégel WILDNEXUS_DEVICE confirmé au pilotage (décision JC) — etat-projets.md et priorites-actives.md alignés ; gates de reprise à lever avant montage/achat |
| 2026-11-11 | P0 engineering repris (décision JCH) ; SOP-16/17/18 créées, ADR-018 référencé, caveats sécurité SOP-08/09/13 |
| 2026-11-10 | Skill caméra réaligné sur ADR-002 : OV5640 P0, IMX462 repli P1, interface DVP (pas MIPI) |
| 2026-11-05 | Firmware destiné à MIT + `ETHICS.md` et politique d'usage ; ce n'est pas une dual-licence. Autres objets de licence à traiter séparément. |
| 2026-11-05 | Prix FIELD 149–179 € et marge 40 % retirés provisoirement ; coût produit complet inconnu. |
| 2026-11-05 | 60 jours, IP67, portée et latence traités comme cibles ; preuves matérielles exigées. |
| 2026-07-05 | Double cycle caméra/audio, payload spectral et format audio définis dans ADR-014/016/017. |
| 2026-06-19 | Couche acoustique stéréo définie dans ADR-013. |
| 2026-06-14 | Wokwi retenu comme smoke test, sans valeur de validation matérielle. |

## TTD — Done

- [x] 2026-11-22 · SOP-01 Phase A (`wn_blink`) re-validé sur M5 — flash + moniteur série via arduino-cli ; carte identifiée (ESP32-S3 QFN56 rev v0.2, MAC 58:e6:c5:74:7d:2c, flash 8MB quad Micron, PSRAM 8MB OPI). Outillage : Arduino IDE 2.3.10 + esp32 core 3.3.10.
- [x] 2026-11-22 · SOP-02 Phase B (`wn_deep_sleep_30s`) re-validé sur M5 — cycle deep sleep 30 s confirmé : 4 réveils, intervalles 31,0 s (30 s sommeil + 1 s delay), reset `rst:0x5 (DSLEEP)` à chaque réveil.
- [x] 2026-11-22 · SOP-03 Phase C (PPK2 deep sleep) re-validé sur M5 — PPK2 piloté en CLI (ppk2-api 0.9.2, Source Meter 5 V) : deep sleep **1061 µA** (médiane), pic boot **158 mA**, cycle 30,0 s. Confirme l'overhead DevKit ~1 mA (AMS1117 + LEDs + CP2102) — ESP32-S3 seul estimé <20 µA, à re-mesurer sur PCB nu.
- [x] 2026-11-22 · SOP-04 Phase D (`wn_wake_short` 20 cycles) re-validé sur M5 — 20/20 cycles au moniteur série (intervalle 17,5 s stable, zéro blocage) + 6/6 cycles mesurés au PPK2 (deep sleep 1062 µA, pic boot ~155 mA, durée active ~2,55 s). ✅ GO.
- [x] 2026-11-12 · Checklist d'inventaire de reprise préparée (`07_PROCUREMENT_BOM/INVENTAIRE-checklist-reprise-2026-11-12.md`) — gate 1 prête à exécuter au banc.
- [x] 2026-11-10 · Skill wildnexus-camera-imaging réaligné sur ADR-002 (OV5640 P0 / IMX462 P1 / DVP) + graphe graphify nettoyé des chemins WildNexus obsolètes.
- [x] 2026-11-05 · Analyse fraîche du scope, des preuves et des incohérences documentaires ; cibles non mesurées distinguées des résultats acquis.
- [x] 2026-11-05 · Organisation du projet et documents de cadrage consolidés ; gel WildNexus, suspension de SOP-10 et pause des achats maintenus.

## Historique sessions

| Date | Résumé | Livrable |
|------|--------|----------|
| 2026-11-22 | SOP-01→04 (Phases A/B/C/D) re-validées sur M5 — flash + moniteur série via arduino-cli, mesure PPK2 via ppk2-api ; carte identifiée ; règle outillage consignée (CDC off + compile --clean) | `MEMORY.md`, `thread-wildnexus.md`, `~/Documents/Arduino/wn_blink/`, `~/Documents/Arduino/wn_deep_sleep_30s/`, `~/Documents/Arduino/wn_wake_short/` |
| 2026-11-10 | Correction dérive caméra (skill vs ADR-002) + nettoyage graphe graphify (chemins WildNexus obsolètes) | `07_AGENTS/Agents/wildnexus-camera-imaging/SKILL.md`, `graphify-out/graph.json`, `wiki/Daily/2026/11/2026-11-10-cozmo-compagnon-ia-corrections-wildnexus-caméra-et-graphe.md` |
| 2026-11-05 | Revue documentaire et organisationnelle complète, sans reprise firmware, matériel ou achats | `thread-wildnexus.md`, `00_GOVERNANCE/Start.md`, `wiki/Daily/2026/11/2026-11-05-stabilisation-zigbee-rpi-et-revue-multiprojet.md` |

Les sessions de juin et juillet ont restructuré le projet et produit le firmware testé sur hôte. Les dates d'achat et les états matériels détaillés dans les anciens documents doivent être confirmés physiquement à la reprise. Les archives ne sont pas réécrites comme si elles décrivaient l'état actuel.

## Liens depuis `JCH_Inbox/`

- Démarrage : `03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/00_GOVERNANCE/Start.md`
- Scope : `03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md`
- ADR : `03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/02_DECISIONS/WILDNEXUS_ADR_INDEX.md`
- Progrès : `03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/03_P0_ENGINEERING/PROTOCOLES/progress.md`
- Budget : `03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/03_P0_ENGINEERING/08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md`
- Achats/BOM : `03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/03_P0_ENGINEERING/07_PROCUREMENT_BOM/`
- Matériel PKA : `04_PILOTAGE_STRATEGIQUE/hardware-state.md`
- Projet ombrelle : `03_PROJECTS/03_WILDNEXUS/README.md`
- InsectNet : `03_PROJECTS/03_WILDNEXUS/INSECTNET/`
- NEXUS_ACOUSTIC : `03_PROJECTS/03_WILDNEXUS/NEXUS_ACOUSTIC/`
- Planning : `03_PROJECTS/03_WILDNEXUS/PLANNING_GANTT.md`