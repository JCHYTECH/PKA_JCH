# Diagnostic consolidé — RPi 5 Lupo boot bloqué

> **Date :** 2026-10-01 | **Orchestré par :** Dobby 🦉
> **Objet :** consolider les blocages RPi 5 (juillet + septembre 2026) en une source unique. Les diagnostics de septembre n'avaient pas été archivés — ce fichier répare ce trou.

---

## 1. Matériel en jeu

| Composant | État |
|-----------|------|
| RPi 5 4GB | Assemblé : X1205 UPS HAT (pogo pins) + NVMe Shield + SSD Fanxiang 256GB + X1201-C1 + PV PI HAT |
| MicroSD | Samsung PRO Endurance 256GB (reçue 17/07) — remplace la 128GB d'origine |
| NVMe | Fanxiang 256GB — wipé le 13/07 (ex-HA OS, passé HFS+) |
| Alim | Officielle 27W USB-C (X1205 pogo pins insuffisants pour boot NVMe) |

## 2. Historique des blocages

### Juillet 2026 (résolu en partie)
- HA OS 18.x + RPi 5 + NVMe hat = bug GitHub #4785 → I/O errors ~3 min, filesystem corrompu. **RÉSOLU : cause racine #5005 (nvme_free_sgls) corrigée dans HAOS 18.3 (17/09/2026).** Ne plus rester sur 17.3 — flasher 18.3.
- Duplicate OS : microSD (auto-updatée 18.1) + NVMe (17.3) → système « Unhealthy ».
- Décision 11/07 : **SD boot uniquement** (pas de NVMe), hostname `lupo`, `ha supervisor repair`, NVMe retiré physiquement.

### Septembre 2026 (non résolu, non archivé)
| Bloqueur | Détail |
|----------|--------|
| Boot gelé phase init hardware | RPi figé au démarrage, aucune progression vers l'OS |
| SQUASHFS NVMe | `fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5` — partition corrompue ou image erronée |
| duplicate_os_install | Réapparu — `AppManager.install` bloqué, instance HA fantôme |
| SSH perdu | « Broken pipe », accès terminal impossible |
| Image HAOS | `haos_rpi5-15.1.img` introuvable (404/timeout download) — utiliser **17.3**, pas 15.1 ni 18.x |
| PSU_MAX_CURRENT | Tenté =5000 (config X1205) — non concluant |

⚠️ **Incohérence à lever :** juillet disait « NVMe retiré », septembre mentionne `nvme0n1p5`. Le NVMe est-il remonté ? À confirmer physiquement.

## 3. Cause racine probable

1. **Bug #4785** : HA OS 18.x + NVMe = corruption filesystem (si le NVMe est toujours dans le stack).
2. **Conflit microSD/NVMe** : deux installs HA → `duplicate_os_install`.
3. **Image HAOS erronée/incomplète** : téléchargements timeout, `generic` vs `rpi5-64`, checksum non vérifié.

## 4. Plan de déblocage (recommandé : SD seule, reflash propre 18.3)

### Phase A — Vérité terrain (physique)
1. Éteindre le RPi 5 (débrancher l'alim USB-C).
2. Ouvrir le boîtier X1201-C1.
3. Constater : NVMe présent ou retiré ? Quelle microSD (128 ou 256 Endurance) ?

### Phase B — Boot microSD seule (propre)
1. Télécharger `haos_rpi5-64-18.3.img` (dernière stable, inclut le fix #5005) — PAS `generic-aarch64` — + vérifier SHA256. Contournement si 18.0-18.2 : `nvme.sgl_threshold=0`.
2. Flasher la microSD Endurance 256GB.
3. Booter **microSD seule** (NVMe retiré physiquement).
4. Onboarding : désactiver l'auto-update immédiatement (Settings → System → Updates → OFF), hostname `lupo`.
5. Vérifier statut « Healthy ».

### Phase C — NVMe data disk (plus tard, optionnel)
1. Wiper le NVMe (via M5 + adaptateur USB).
2. Réinsérer, `Move Data Disk` → NVMe.
3. Surveiller les I/O errors (#4785) avant de valider pour le van.

### Phase D — Installation van (deadline 15/12)
- Silentblocs + coating + câblage 12V + PV PI + capteurs Zigbee.

## 5. Points à confirmer par JC (bloquants pour démarrer)

1. **NVMe** : toujours monté dans le stack, ou retiré depuis juillet ?
2. **MicroSD** : laquelle est en place (128GB d'origine ou 256GB Endurance) ?
3. **Boot actuel** : quand tu allumes, qu'est-ce qui se passe exactement (LED verte, affichage, apparition sur le réseau) ?

---

## 6. RÉSOLU — 2026-10-01

- **Cause confirmée :** le NVMe (remonté dans le stack) détournait le boot → SQUASHFS `nvme0n1p5` + boot gelé.
- **Action :** NVMe retiré physiquement, boot sur microSD seule (Samsung PRO Endurance 256GB).
- **Résultat :** RPi 5 boote, HA OS **Healthy** (Supervisor Connected · Support Supported · Health Healthy), HA joignable (HTTP 200), Tailscale `lupo` online.
- **Mise à jour 01/10 :** HAOS 17.3 → **18.3** via `ha os update` (après `ha supervisor update` 2026.07.3 → 2026.09.3). **Auto-update désactivé** (`auto_update: false`). Core 2026.7.2 → **2026.9.4** (13:53). Stack complet à jour : OS 18.3 · Supervisor 2026.09.3 · Core 2026.9.4. `Healthy`, `Supported`.

---

*Consolidé par Dobby 🦉 — à mettre à jour après chaque étape de déblocage.*
