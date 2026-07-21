# Diagnostic — Duplicate OS Installation — Lupo RPi 5

> **Date :** 2026-07-10 | **Session :** Dobby 🦉 — analysé et corrigé par Dobby + Forge 🔨 + Araignée 🕷️
> **Statut :** ⚠️ Non résolu — Plan d'action défini ci-dessous
> **Problème :** Deux installations HA OS coexistent (microSD 18.1 + NVMe 17.3), le système est « Unhealthy »

---

## 1. Ce qui s'est passé

- Le 9 juillet, HA OS 17.3 a été installé avec succès sur le **NVMe** (après correction de l'image `generic` → `rpi5-64`)
- Le 10 juillet, JC voulait fiabiliser le boot en passant à **microSD boot + NVMe data** (pour éviter les pogo pins X1205 instables en van)
- Flash de `haos_rpi5-64-17.3.img` sur la **microSD**
- Le RPi a booté, HA OS s'est lancé, **a détecté le Wi-Fi via le partage de connexion M5, et s'est auto-mis à jour vers HA OS 18.1**
- Résultat : microSD = HA OS 18.1 frais + NVMe = HA OS 17.3 d'hier → **deux installations OS coexistent** → système « Unhealthy » (duplicate_os_installation)

## 2. Symptômes

- HA fonctionne (interface accessible via `192.168.2.2:8123`) mais est marqué « Unhealthy »
- Le « Move Data Disk » ne propose pas le NVMe car il contient un OS
- L'installation du module Terminal (pour wipe le NVMe) est bloquée car le système est Unhealthy

## 3. ⚠️ Alerte critique — HA OS 18.x sur RPi 5 + NVMe hat

**Rappel du 9 juillet (MEMORY.md) :** Bug **ouvert** GitHub #4785 — HA OS 18.0/18.x + RPi 5 + NVMe hat → I/O errors en ~3 min, filesystem corrompu. **Non résolu au 10 juillet 2026.**

La microSD s'est auto-updatée vers **18.1** — c'est précisément la version à éviter pour Lupo. **Il faut impérativement revenir à HA OS 17.3.**

**Action immédiate :** Désactiver l'auto-update HA OS sur toute nouvelle installation (Settings → System → Updates → désactiver les mises à jour automatiques).

## 4. Solution retenue — Option C (microSD boot + NVMe data)

### Pré-requis
- Adaptateur USB-NVMe (boîtier externe USB → M.2) **OU** accès Terminal SSH sur le RPi
- Image `haos_rpi5-64-17.3.img` (la **17.3**, pas 18.x)

### Procédure — Voie 1 (la plus propre, via M5)

1. **Éteindre le RPi 5** complètement (débrancher l'alimentation)
2. **Retirer le NVMe** physiquement du stack X1205
3. **Retirer la microSD** du RPi 5
4. **Insérer le NVMe dans un adaptateur USB-NVMe** → brancher sur le M5
5. **Wiper le NVMe depuis le M5 :**
   ```bash
   # Identifier le disque
   diskutil list
   # Démonter la partition si montée
   diskutil unmountDisk /dev/diskN
   # Wiper les premiers secteurs (efface partitions + bootloader)
   sudo dd if=/dev/zero of=/dev/rdiskN bs=1M count=100
   ```
6. **Flasher la microSD avec HA OS 17.3** (pas 18.x !) :
   ```bash
   # Sur M5, avec balenaEtcher ou dd
   # Vérifier l'image : doit être haos_rpi5-64-17.3.img (PAS generic-aarch64)
   ```
7. **Insérer la microSD** dans le RPi 5 (NVMe toujours débranché)
8. **Booter le RPi 5** — HA OS 17.3 démarre proprement, seul disque → pas de conflit
9. **Désactiver l'auto-update** immédiatement : Settings → System → Updates → OFF
10. **Éteindre le RPi 5**
11. **Reconnecter le NVMe** dans le stack X1205
12. **Booter** — HA OS 17.3 démarre sur microSD, NVMe est vide → pas de conflit
13. **Move Data Disk :** Settings → System → Storage → Move Data Disk → sélectionner le NVMe
14. **Vérifier** que le système passe à « Healthy » et que le data disk est sur NVMe

### Voie 2 (si pas d'adaptateur USB-NVMe)

1. **Éteindre le RPi 5** et retirer le NVMe physiquement
2. **Flasher la microSD** avec `haos_rpi5-64-17.3.img`
3. **Booter sur microSD seule** → HA OS 17.3 propre, pas de conflit
4. **Désactiver l'auto-update** immédiatement
5. **Activer SSH / Terminal** : Settings → Add-ons → Installer « Terminal & SSH »
6. **Éteindre**, reconnecter le NVMe
7. **Booter** → HA OS démarre sur microSD, NVMe contient encore 17.3
8. **Via Terminal (SSH) :**
   ```bash
   # Identifier le NVMe
   lsblk
   # Wiper le NVMe (efface l'OS et les partitions)
   sudo dd if=/dev/zero of=/dev/nvme0n1 bs=1M count=100
   # OU plus propre : effacer la table de partitions
   sudo sgdisk --zap-all /dev/nvme0n1
   ```
9. **Rebooter** → Move Data Disk devrait maintenant proposer le NVMe (vide)
10. **Move Data Disk → NVMe** et vérifier statut « Healthy »

### Voie 3 (fallback rapide — NVMe seul, comme le 9 juillet)

Si les procédures ci-dessus prennent trop de temps et que JC veut juste un système fonctionnel pour avancer :

1. **Retirer la microSD** du RPi 5
2. **Booter sur NVMe seul** → HA OS 17.3 d'hier démarre (pas de conflit)
3. **Désactiver l'auto-update** immédiatement (pour éviter le passage à 18.x)
4. Le boot NVMe direct fonctionne — le risque pogo pins X1205 reste, mais le système est sain
5. La migration microSD boot + NVMe data peut se faire plus tard, sans urgence

> ⚠️ **Cette option réintroduit le risque pogo pins X1205** identifié le 9 juillet. Acceptable pour proto banc, pas pour usage van définitif.

## 5. Leçons apprises

- **Ne jamais laisser HA OS s'auto-updater** — désactiver les updates immédiatement après premier boot (surtout avec le bug 18.x + NVMe hat non résolu)
- **Toujours retirer les autres disques** avant de flasher une nouvelle installation HA OS
- Le partage de connexion M5 → RPi donne internet au RPi → auto-update déclenché → **aggrave la situation**. Si on ne veut pas d'update, couper le partage connexion pendant le premier boot, OU désactiver l'auto-update avant de connecter internet.
- **L'image `haos_rpi5-64-xx.img`** (pas `generic-aarch64`) — le rappeler à chaque flash
- L'approche YOLO n'est pas adaptée quand la navigation UI est le bottleneck — les systèmes HA OS méritent une procédure écrite suivie pas à pas

## 6. État actuel du matériel

| Composant | État |
|-----------|------|
| RPi 5 | Sous tension, accessible via `192.168.2.2:8123` (partage connexion M5) |
| MicroSD | HA OS 18.1 (⚠️ version à éviter — bug #4785) |
| NVMe | HA OS 17.3 (ancienne install du 9 juillet) |
| Stack X1205 | Monté sur RPi 5 (pogo pins — stabilité à vérifier) |
| Proxy socat/Python | Arrêté (plus nécessaire, IPv4 direct) |

---

## 7. Résumé actionnable pour JC

1. **Éteindre le RPi**, retirer NVMe + microSD
2. **Wiper le NVMe** (via M5 + adaptateur USB, ou plus tard via Terminal)
3. **Flasher microSD** avec `haos_rpi5-64-17.3.img` (PAS 18.x, PAS generic)
4. **Booter microSD seule** → HA OS 17.3 propre
5. **Désactiver auto-update** immédiatement après onboarding
6. **Reconnecter NVMe** → Move Data Disk → NVMe
7. **Vérifier statut Healthy** ✅

*Corrigé par Dobby 🦉 le 2026-07-10 — Forge 🔨 : procédure technique — Araignée 🕷️ : validation hardware*
