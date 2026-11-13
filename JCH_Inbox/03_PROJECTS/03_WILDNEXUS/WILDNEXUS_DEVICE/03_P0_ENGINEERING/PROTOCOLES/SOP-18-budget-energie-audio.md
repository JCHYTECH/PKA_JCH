# SOP-18 — Phase R : Budget énergétique audio (PPK2)

**SOP :** SOP-18
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel
**Phase :** R — Mesure PPK2 du pipeline audio (I2S, FFT, WAV+JSON, sommeil)
**Durée :** ~40 minutes
**Prérequis :** SOP-13/15 (audio), PPK2 (SOP-03)
**Auteur :** [[Dobby]]
**Date :** 2026-11-11
**Version :** 1.0 — aucune estimation ne vaut résultat

---

## Objectif

Mesurer l'énergie consommée par chaque étape du pipeline audio sur cible réelle — initialisation I2S, capture 3 s stéréo, FFT, écriture WAV+JSON sur SD, retour en sommeil — pour alimenter WP03 (scénario 60 jours).

> ⚠️ **Aucune estimation ne vaut résultat.** Les délais simulés de SOP-05 ne représentent ni les micros réels, ni la SD, ni les pics de courant. Seules les mesures PPK2 sur matériel identifié comptent.

---

## Matériel

Identique à SOP-15 (Config C : micros + SD, caméra déconnectée) + PPK2 en source meter (sortie OFF avant toute modification).

---

## Mesures à consigner (Wh et mAh)

| Étape | Mesure |
|-------|--------|
| Boot + init I2S | courant + durée |
| Capture 3 s (2 micros) | courant + durée |
| FFT 1024 + 10 features | courant + durée |
| Écriture WAV (192 000 octets) + JSON | courant + durée |
| Retour deep sleep | courant de veille |
| **Total cycle audio** | **Wh / cycle** |

---

## Grille de décision

- ✅ toutes les étapes mesurées séparément et le total cycle documenté → budget audio acquis.
- ✅ valeurs injectées dans WP03 pour le scénario 60 jours.
- ❌ estimation à partir d'un courant supposé ou d'un délai simulé → non valide.

---

*Créé le 2026-11-11 — contenu identifié dans `progress.md` §4 depuis le 2026-07-05. Aucune mesure PPK2 audio n'existe à ce jour.*
