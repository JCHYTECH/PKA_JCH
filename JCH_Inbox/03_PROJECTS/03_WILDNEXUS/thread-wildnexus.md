# Thread — WILDNEXUS

> Living document — mis à jour automatiquement par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-07-05 — Audit P0 ↔ InsectNet/NEXUS_ACOUSTIC, ADR-014/016/017 acceptés
> **Statut** : 🟡 firmware — double cycle caméra+audio

---

## Vue d'ensemble

Nœud caméra-piège IA autonome (ESP32-S3 + OV5640 + LoRa + micros stéréo). Phase M-02 banc actif — budget 1000€. 17 ADRs créés (14 acceptés, 1 sous réserve, 2 proposés). Machine d'états firmware double cycle (caméra PIR + audio timer).

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🟡 | Firmware en développement, tests banc à lancer |
| Hardware | 🟢 | PPK2 ✅, ESP32-S3 ✅, ESP32-CAM ✅, OV5640 ✅, Mouser #39492997 ✅, Miuzei kit ✅, MP1584 ×5 ✅, SPH0645LM4H-B ×2 ✅ |
| Software | 🟡 | Wokwi smoke tests OK, ADR-016 double cycle accepté, firmware repo à créer |
| Audio | 🟡 | ADR-013/014/016/017 acceptés — format WAV + payload spectral définis. SOPs 13-18 ajoutées au tracker. Pas encore exécutées. |
| Documentation | 🟢 | 17 ADRs, Start.md v0.3, scope lock v0.4 |
| Procurement | 🟡 | Panier Mouser restant (~279€) ⏳ À COMMANDER — bloque LoRa (SOP-07) + payload spectral (SOP-16) |

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-07-05 | ADR-014/016/017 acceptés | Audit portes fermées WildNexus ↔ InsectNet/NEXUS_ACOUSTIC. Double cycle firmware, payload spectral, format audio WAV. |
| 2026-06-30 | ADR-016 firmware intégré créé | Architecture firmware unifiée (complété avec cycle audio le 05/07) |
| 2026-06-19 | ADR-013 micros stéréo acceptés | Couche acoustique P0 + upgrade path ICS-43434 |
| 2026-06-14 | Wokwi adopté comme smoke test CI | Logique firmware sans hardware |
| 2026-06-12 | Skills politique de shadow | Skills locaux > skills fondation |

---

## Prochaine étape

**Action prioritaire** : Commander panier Mouser (~279€) — débloque LoRa (SOP-07) + payload spectral (SOP-16)
**Action parallèle** : Créer repo `wildnexus-firmware/` (FW-01) + implémenter codec ADR-014 (FW-02, pas de hardware requis)
**Deadline caméra** : 15 juillet — test harness (CAM-03)
**Deadline audio** : SOP-13 (I2S init) peut démarrer dès que le pinout I2S est mappé — pas bloqué par Mouser

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-07-05 | Audit P0 WildNexus ↔ InsectNet/NEXUS_ACOUSTIC. 7 portes ouvertes, 1 fermée (audio), 4 étroites. ADR-014/016 révisés, ADR-017 créé. 3 ADRs acceptés. SOPs 13-18 + FW-01 à FW-05 ajoutés au tracker. | `TEAM_Inbox/2026-07-05_dobby_audit-p0-wildnexus-insectnet-nexus-acoustic.md` |
| 2026-06-30 | Nettoyage projet complet, ADR-016, Start.md v0.3 | — |
| 2026-06-19 | Réorganisation WildNexus (extraction NEXUS_ACOUSTIC) | `TEAM_Inbox/2026-06-19_dobby_analyse-reorganisation-wildnexus.md` |

---

## Liens

- INDEX : `03_PROJECTS/03_WILDNEXUS/`
- ADRs : `03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/` (17 ADRs)
- Hardware : `hardware-state.md` (section WildNexus P0)
- Procurement : `03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/07_PROCUREMENT_BOM/`
- Progress : `03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/PROTOCOLES/progress.md`
- Audit : `TEAM_Inbox/2026-07-05_dobby_audit-p0-wildnexus-insectnet-nexus-acoustic.md`
- InsectNet : `03_PROJECTS/09_InsectNet/`
- NEXUS_ACOUSTIC : `03_PROJECTS/12_NEXUS_ACOUSTIC/`

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`.*
