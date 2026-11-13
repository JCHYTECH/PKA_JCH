# SOP-17 — Phase Q : Coexistence PIR + timer audio

**SOP :** SOP-17
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel
**Phase :** Q — Test coexistence réveil PIR + capture audio programmée (ADR-016 double cycle)
**Durée :** ~30 minutes
**Prérequis :** SOP-04 (réveil court), SOP-09 (PIR), SOP-13/15 (audio)
**Auteur :** [[Dobby]]
**Date :** 2026-11-11
**Version :** 1.0 — routage testé hôte uniquement ; concurrence matérielle à mesurer

---

## Objectif

Vérifier que le double cycle ADR-016 — réveil PIR (cycle caméra) et capture audio timer-triggered — coexiste sans contention matérielle ni conflit de GPIO, et mesurer le timing réel des transitions.

> ⚠️ **Config D (cycle complet simulé).** LoRa + I2S + SD connectés, caméra **simulée en firmware** (non câblée). GPIO 6/7 (I2S) et GPIO 4 (PIR) sont alors libres des lignes DVP. La caméra physique reste exclue de cette SOP.

---

## Conflits à respecter (`wn_config.h`)

| GPIO | Périphérique 1 | Périphérique 2 | Règle |
|------|----------------|----------------|-------|
| 4 | PIR | Camera D0 | Config A : PIR déclenche puis caméra prend D0 |
| 6 | I2S DIN1 | Camera D2 | exclusif — caméra déconnectée en Config C/D |
| 7 | I2S DIN0 | Camera D3 | exclusif — caméra déconnectée en Config C/D |

---

## Test

1. Config D : LoRa + I2S + SD, caméra déconnectée.
2. Armer un réveil timer (cycle audio) et le PIR (cycle caméra simulé).
3. Provoquer un déclenchement PIR **pendant** une capture audio, puis l'inverse.
4. Journaliser chaque transition SLEEP→WAKE→CAPTURE→STORE→TX→SLEEP avec horodatage.

---

## Grille de décision

- ✅ les deux cycles se déclenchent sans corruption de capture ni blocage → coexistence validée sur cible.
- ✅ latence de réveil, durée de capture et retour sommeil mesurés et consignés.
- ❌ contention observée (I2S tronqué, PIR manqué, reboot) → documenter et arbitrer la matrice GPIO (ADR-016 / ADR-008).

---

*Créé le 2026-11-11 — contenu identifié dans `progress.md` §4 depuis le 2026-07-05. La concurrence matérielle réelle n'est pas encore démontrée.*
