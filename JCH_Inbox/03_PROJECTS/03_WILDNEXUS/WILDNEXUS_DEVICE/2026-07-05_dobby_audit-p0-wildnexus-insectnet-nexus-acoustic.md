# 2026-07-05 — Dobby : Audit P0 WildNexus ↔ InsectNet/NEXUS_ACOUSTIC

> **Auteur :** Dobby 🦉
> **Date :** 2026-07-05
> **Spécialistes mandatés :** Forge 🦦 (ADR-016/014), Dobby (ADR-017), Chouette 🦉 (validation formats)
> **Contexte :** JC a demandé une revue du P0 WildNexus en gardant en vue les projets InsectNet et NEXUS_ACOUSTIC. Objectif : s'assurer qu'aucune porte n'est fermée.

---

## Contexte de la revue

WildNexus P0 est en phase M-02 (prototype banc). Les 16 ADRs existants définissent un nœud caméra ESP32-S3 + OV5640 + LoRa + micros stéréo. InsectNet et NEXUS_ACOUSTIC ont été extraits de WildNexus le 19/06 comme projets autonomes, mais la couche d'interface entre le hardware P0 et les pipelines aval n'avait jamais été auditée.

## Méthode

Lecture intégrale de :
- 16 ADRs (ADR-001 à ADR-016)
- MASTER_ARCHITECTURE_WN (518 lignes)
- WILDNEXUS_P0_SCOPE_LOCK v0.3
- Start.md v0.3 (gouvernance opérationnelle)
- PROTOCOLES/progress.md (tracker M-02)
- 3 executive summaries (WildNexus, InsectNet, NEXUS_ACOUSTIC)
- Product sheets (F1/F2/S1/S2/A1)
- Projet_bioacoustique.md (Document Unique NEXUS_ACOUSTIC)
- Structure LEAFNET
- Registre hardware NEXUS_ACOUSTIC

## Constat : 7 portes ouvertes, 1 fermée, 4 étroites

### Portes correctement ouvertes (7)
1. MCU avec fallback STM32U5/RV1106 (ADR-001)
2. Caméra M12 interchangeable (ADR-002)
3. Bus capteurs I2C/SPI/UART + volume réservé (ADR-008)
4. Architecture Satellite → Base → Cloud (ADR-009) — la Base RPi = pont NEXUS_ACOUSTIC
5. Micros avec upgrade ICS-43434 pin-compatible (ADR-013)
6. Module wn_audio listé dans l'arborescence firmware (ADR-016)
7. Gamme produit A1 Nexus Acoustic dans la roadmap

### Porte fermée — corrigée (1)
**ADR-016 machine d'états : aucun état AUDIO.** Le cycle firmware était SLEEP→WAKE(PIR)→CAPTURE→AI→STORE→TX→SLEEP. Aucun timer pour la capture audio programmée. Les micros auraient été muets. **Corrigé** : ajout d'un double cycle (caméra PIR + audio timer) avec gestion des conflits.

### Portes étroites — corrigées (4)
1. **ADR-014 payload LoRa : pas de type spectral** → ajouté 0x05 + format 48 bytes avec 10 descripteurs
2. **Pas de schéma métadonnées audio** → ADR-017 créé (WAV PCM 16-bit 16kHz stéréo + sidecar JSON)
3. **Pas de synchronisation temporelle image↔audio** → ADR-018 identifié (backlog, NTP P0 + RTC DS3231 P1)
4. **Taille SD non spécifiée** → ADR-017 recommande 128 GB minimum

## Actions livrées (3 ADRs modifiés/créés)

### 1. ADR-016 révisé — Machine d'états double cycle
- Ajout cycle AUDIO FFT (timer 15 min) : AUDIO_WAKE → AUDIO_FFT → AUDIO_STORE → TX_LORA (spectral) → SLEEP
- Ajout cycle AUDIO CLIP (timer 60 min) : AUDIO_WAKE → AUDIO_RECORD (3s WAV) → AUDIO_STORE → SLEEP
- Gestion des conflits PIR/timer (priorité caméra, différé audio)
- Budget énergétique audio : ~1,4 mAh/jour (20% du budget caméra)
- 4 nouveaux tests obligatoires (cycle FFT, cycle CLIP, conflits, WAV valide)
- Nouveau module `wn_audio_metadata.c` dans l'arborescence
- Nouveau fichier de test `test_audio_cycle.c`

### 2. ADR-014 révisé — Payload LoRa multi-type
- Event type 0x05=spectral ajouté
- Format payload spectral 48 bytes : 10 descripteurs quantifiés u16 + métadonnées audio
- Flag audio_clip_ready (bit4) dans le bitfield Flags
- Commandes downlink 0x05 (upload_audio_clip via Wi-Fi) et 0x06 (set_audio_schedule)
- Règle de priorité : caméra > spectral dans la queue FIFO

### 3. ADR-017 créé — Schéma métadonnées audio
- Format : WAV PCM 16-bit, 16 kHz, stéréo (compatible BirdNET, InsectSet459, TweetyBERT)
- Convention nommage : `AUDIO/{NODE_ID}/{YYYY}/{MM}/{DD}/{NODE_ID}_{YYYYMMDD}_{HHMMSS}_{TYPE}.wav`
- Sidecar JSON : schema_version, audio params, microphones, environment, spectral_features, detection, integrity
- Sidecar JSON spectral (FFT 15 min) : compact, pas de WAV
- Structure SD : `DCIM/` (images) + `AUDIO/` (audio) séparés
- Recommandation SD 128 GB minimum (~8 jours monitoring continu P1)
- Compatibilité vérifiée : BirdNET-Lite ✅, InsectSet459 ✅ (resample), TweetyBERT ✅, SoundPlot ✅
- Chiffrement AES-128 (ADR-010) applicable, désactivable en M-02 pour tests

### 4. Documents mis à jour
- WILDNEXUS_ADR_INDEX : v0.8 → v0.9 (17 ADRs, ADR-017 ajouté, ADR-018 backlog)
- WILDNEXUS_P0_SCOPE_LOCK : v0.3 → v0.4 (cycles audio précisés, interfaces préservées élargies)

## Compatibilité pipelines aval — tableau final

| Pipeline | Format WildNexus P0 | Compatibilité | Conversion requise |
|----------|-------------------|---------------|-------------------|
| BirdNET-Lite (RPi 5) | WAV 16kHz/16-bit/stéréo | ✅ Direct | Aucune (stéréo→mono auto) |
| InsectSet459 fine-tuning | WAV 16kHz/16-bit/stéréo | ✅ | `ffmpeg -i in.wav -ac 1 out.wav` |
| TweetyBERT (M5) | WAV 16kHz/16-bit/stéréo | ✅ Direct | librosa gère tous formats |
| SoundPlot (3D viz) | WAV + JSON sidecar | ✅ Direct | JSON fournit timestamps |

## Impact sur le budget P0

| Item | Coût | Impact |
|------|------|--------|
| Carte microSD 128 GB (vs 32 GB) | +7€ | Dans la réserve 111€ |
| Budget énergétique audio | +1,4 mAh/jour | ~20% du budget caméra — acceptable |
| Pas d'autre impact hardware | 0€ | Les micros sont déjà dans le BOM (ADR-013) |

## ADR-018 identifié (backlog, non livré)

Synchronisation temporelle image↔audio. L'ESP32-S3 n'a pas de RTC hardware — dérive 2-5% en deep sleep. P0 : NTP au provisioning (BLE/Wi-Fi). P1 : RTC externe DS3231 (~2€) dans le volume réservé PCB (ADR-008). À rédiger avant M-03.

---

*Livrable généré par Dobby 🦉 le 2026-07-05. Spécialistes : Forge 🦦 (révisions ADR technique), Chouette 🦉 (validation format bioacoustique). Audit basé sur lecture intégrale de 16 ADRs + MASTER_ARCHITECTURE + scope lock + 3 executive summaries + product sheets + progress tracker.*
