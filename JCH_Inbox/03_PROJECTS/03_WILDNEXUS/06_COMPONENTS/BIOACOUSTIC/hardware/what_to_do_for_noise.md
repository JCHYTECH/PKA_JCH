# What to do for noise — Traitement post-production audio BirdNET

> **STATUT : ABANDONNÉ** — 2026-06-05
> Décision JCH : le projet de nettoyage audio RNNoise est arrêté.
> Raison : RNNoise entraîné sur voix humaine (300 Hz–3,4 kHz) — incompatible avec les chants d'oiseaux (2–8 kHz). Le filtre `arnndn` était également indisponible dans l'environnement cron. Le besoin métier reste ouvert si une solution plus adaptée (`afftdn` ou autre) est priorisée un jour.
> **Cleanup effectué :** crontab retiré, script archivé → `JCH_Inbox/07_ARCHIVES/rnnoise-overnight.sh`, fichiers techniques supprimés (log, modèle `.rnn`, raw/*).

**Date :** 2026-06-04
**Projet :** WildNexus / Bioacoustique
**Contexte :** Discussion Qwen 3.7 (local Ollama) → [[Dobby]]/[[Forge]] → implémentation RNNoise batch
**Fichiers liés :** `BIRDNET_PI_ACCESS.md`, `Projet_bioacoustique.md`

---

## Problème

BirdNET-Pi capture de l'audio 24h/24. Les fichiers bruts contiennent du bruit de fond (vent, route, insectes non-cibles) qui :
- dégrade la qualité des détections BirdNET
- rend les écoutes de validation moins confortables
- consomme de l'espace disque inutilement

## Solution retenue : RNNoise batch nocturne (v6)

Pipeline quotidien complet : sync RPi → RNNoise → purge. Lancement à 3h00 par cron.

### Architecture

```
RPi (BirdNET-Pi)
/home/jchavaux/BirdSongs/StreamData/   ← WAV 24h/24 (segments 3-15s)
                │
                │ rsync via Tailscale (100.66.110.60)
                ▼
~/PKA_JCH/_local/audio/raw/           ← entrée WAV synced
                │
                │ Phase 2 : RNNoise (ffmpeg arnndn)
                ▼
~/PKA_JCH/_local/audio/clean/         ← sortie _clean.wav

    Log    → rnnoise-overnight.log
    Lock   → /tmp/rnnoise-overnight.lock
    Modèle → ~/PKA_JCH/_local/audio/rnnoise_model.rnn
```

### Script : `rnnoise-overnight.sh` (v6 — déployée)

| Phase | Description |
|-------|-------------|
| 1 - rsync | Pull des WAV du RPi (`jchavaux@100.66.110.60`) vers `raw/` via Tailscale. Filtre : audio seulement. |
| 2 - RNNoise | `ffmpeg arnndn` sur les fichiers de la veille (J-1), priorité `nice -n 10` |
| 3 - Purge | Raw > 30 jours supprimés + orphelins clean/ nettoyés |

| Paramètre | Valeur |
|-----------|--------|
| Plage traitée | Veille uniquement (J-1 00:00 → 23:59) |
| Formats | WAV, FLAC |
| Skip fichiers | ouverts (lsof), déjà traités, erreurs |
| Priorité | `nice -n 10` |
| Modèle | `~/PKA_JCH/_local/audio/rnnoise_model.rnn` (293 KB, voix générique GregorR) |
| Purge raw | > 30 jours |
| Verrouillage | `noclobber` (macOS natif) |
| Notification | macOS Desktop si échecs > 0 |

### Crontab (à installer manuellement)

```bash
(crontab -l 2>/dev/null | grep -v "rnnoise-overnight.sh"; echo "0 3 * * * bash /Users/jchavauxm5/PKA_JCH/scripts/rnnoise-overnight.sh") | crontab -
```

### Prérequis vérifiés

- ✅ SSH key `id_ed25519` sur le Mac, déployée sur le RPi
- ✅ Connexion Tailscale au RPi : `100.66.110.60` (rpi-pkajch)
- ✅ `ffmpeg` 8.1.1 avec filtre `arnndn` (brew)
- ✅ Modèle `.rnn` téléchargé (GregorR, `beguiling-drafter-2018-08-30`)
- ✅ Script v6 exécutable et testé : rsync OK, boucle RNNoise OK

---

## État des actions

### ❌ Bloquant — Modèle `.rnn` manquant

Le script est déployé, le cron installé, mais **sans fichier `rnnoise_model.rnn`** dans `~/PKA_JCH/_local/audio/`, ffmpeg ne peut pas exécuter le filtre `arnndn`.

**Sources possibles à investiguer :**
1. [GregorR/rnnoise-models](https://github.com/GregorR/rnnoise-models) — modèles génériques (voix, musique)
2. Modèle spécialisé chants d'oiseaux / bioacoustique — à rechercher
3. Entraînement custom (Phase 2 WildNexus si besoin)

### ✅ Déjà fait

- Script `rnnoise-overnight.sh` créé et exécutable
- Crontab installé (nettoie l'ancien, ajoute le nouveau)
- macOS compatibility : flock→noclobber, ionice→nice, lsof natif
- Lockfile, log rotatif, skip stratégiques (fichiers ouverts, déjà traités)

### 📋 Actions à prendre immédiatement

1. **Trouver un modèle `.rnn`** (déléguer à [[Furet]] + [[Clio]] si besoin) et le placer dans `~/PKA_JCH/_local/audio/rnnoise_model.rnn`
2. **Tester le script** : `bash ~/PKA_JCH/scripts/rnnoise-overnight.sh` (créer un fichier factice daté J-1 dans `raw/` d'abord)
3. **Vérifier le log** ensuite : `cat ~/PKA_JCH/_local/audio/rnnoise-overnight.log`
4. **Valider le cron** le lendemain à 3h00 — checker le log au matin
5. **Documenter** le modèle source et sa performance dans ce même fichier

---

## Notes techniques

**Pourquoi pas en temps réel ?** — BirdNET-Pi (RPi 5) CPU limité. RNNoise temps réel ajouterait latence et risking de saturation. Le batch nocturne transfère la charge au Mac M5 local heures creuses.

**Pourquoi pas un filtre passe-haut ?** — `arnndn` est un réseau neuronal plus discriminant. Il supprime le bruit ambiant continu (vent, route, ronron) en préservant les transitoires des chants d'oiseaux. Un passe-haut couperait aussi les harmoniques aiguës.

**Où va le nettoyé ?** — `/BirdSongs_Clean/` à la racine, accessible aux outils (re-scan BirdNET, validation manuelle, training). Raw purgé après 30 jours.

---

*Document [[Dobby]] 🦉 + [[Forge]] 🦦 — suite discussion Qwen 3.7 du 2026-06-04*
