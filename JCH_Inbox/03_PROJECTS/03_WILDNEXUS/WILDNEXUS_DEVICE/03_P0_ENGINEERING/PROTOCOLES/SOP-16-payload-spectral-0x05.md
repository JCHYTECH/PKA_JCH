# SOP-16 — Phase P : Payload spectral 0x05 (codec ADR-014)

**SOP :** SOP-16
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel
**Phase :** P — Encodage du payload spectral `0x05` (ADR-014 v2)
**Durée :** ~25 minutes
**Prérequis :** SOP-14 réussi (features spectrales) ; codec `wn_payload_codec` disponible ; SOP-07 pour l'émission réelle
**Auteur :** [[Dobby]]
**Date :** 2026-11-11
**Version :** 1.0 — codec hôte 13/13 (FW-02) ; émission radio non démontrée

---

## Objectif

Encoder les 10 descripteurs spectraux produits par SOP-14 dans le payload LoRa **48 octets** de type `0x05=spectral` (ADR-014 v2), vérifier le CRC-16 et le compteur de trame, puis rejouer le décodage. L'émission et la réception réelles appartiennent à SOP-07.

> ⚠️ **Preuve radio séparée.** Un roundtrip encode→décode sur hôte ne vaut pas transmission LoRa. Le statut reste `host done / radio pending` tant que SOP-07 n'a pas observé un paquet réel reçu et décodé.

---

## Matériel

Identique à SOP-14 (Config C : micros + SD, caméra déconnectée). Pour l'émission : LoRa SX1262 (Config B/D) — voir SOP-07 et `wn_config.h`.

---

## Format spectral (ADR-014 v2 §3, event type 0x05)

| Champ | Offset | Type | Description |
|-------|:------:|------|-------------|
| Version | 0 | u8 | 0x01 |
| Flags | 1 | u8 | bit4 = audio_clip_ready |
| Node ID | 2 | u32 | identifiant nœud |
| Timestamp | 6 | u32 | Unix UTC |
| Event type | 10 | u8 | **0x05 = spectral** |
| Feature 1–2 | 11–15 | — | centroid, rolloff |
| Feature 3–10 | 16–31 | u16 ×8 | bandwidth, flatness, RMS, ZCR, entropy, peak freq, skewness, kurtosis |
| Audio clip count | 32 | u16 | clips WAV sur SD |
| Battery mV | 34 | u16 | tension batterie |
| Temperature | 36 | i8 | offset −40 |
| Mic status | 37 | u8 | bit0=mic_L_ok, bit1=mic_R_ok |
| Reserved | 38 | u16 | zéro |
| Frame counter | 40 | u16 | incrémental |
| CRC-16 | 42 | u16 | CCITT sur octets 0–41 |
| Padding | 44 | u32 | zéro — alignement 48 |

**10 descripteurs** (ADR-013) : centroid, rolloff, bandwidth, flatness, RMS, zero crossing rate, entropy, peak frequency, skewness, kurtosis.

**Quantification v1** (alignée `wn_config.h`, `WN_FREQ_QUANT_MAX 16000`) : centroid, rolloff, bandwidth, ZCR et peak frequency sur la plage 0–16000 ; les autres échelles suivent le codec v1. Voir ADR-014 §3 pour les offsets exacts et la formule de quantification.

---

## Test hôte (sans matériel)

Le codec `firmware/main/codecs/wn_payload_codec.c` est implémenté et testé :

```bash
cd firmware
gcc -o test/test_payload_codec test/test_payload_codec.c main/codecs/wn_payload_codec.c -Imain
./test/test_payload_codec
```

Attendu : `Results: 8/8 passed` (roundtrip, CRC mismatch, taille fixe).

### Sur nœud (après SOP-14)

1. Récupérer les 10 features + peak frequency de SOP-14.
2. Encoder un payload `0x05` via `wn_payload_codec`.
3. Vérifier `Frame counter` incrémenté et `CRC-16` correct.
4. Si LoRa connecté (SOP-07) : émettre et vérifier le décodage gateway.

---

## Grille de décision

- ✅ roundtrip encode→décode OK + CRC correct + compteur incrémenté → codec validé (hôte).
- ✅ paquet `0x05` reçu et décodé par la gateway (10 features + peak freq) → preuve radio acquise (SOP-07).
- ❌ CRC mismatch ou taille ≠ 48 → corriger l'encodage avant toute émission.

---

*Créé le 2026-11-11 — contenu identifié dans `progress.md` §4 depuis le 2026-07-05. Émission radio renvoyée à SOP-07.*
