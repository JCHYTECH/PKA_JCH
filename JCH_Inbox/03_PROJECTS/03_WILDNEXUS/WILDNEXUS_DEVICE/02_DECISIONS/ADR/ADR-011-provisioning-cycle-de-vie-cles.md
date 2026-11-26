# ADR-011 — Provisioning et cycle de vie des clés

**Date :** 2026-06-08
**Statut :** proposé
**Owner PKA :** [[Castor]] + [[Forge]] + [[Hermine]]
**Agent WildNexus :** `wildnexus-firmware-ulp`
**Jalon :** M-02 Prototype banc · M-03 Firmware ULP (provisioning terrain)

## Contexte

L'ADR-010 exige que chaque nœud possède une clé de chiffrement unique pour la carte SD. Sans diversification, un nœud compromis permet de déchiffrer les SD de toute la flotte. Cette ADR définit la procédure de provisioning — comment les clés sont générées, injectées, stockées et renouvelées — et le cycle de vie complet d'une clé nœud.

## Décision

### 1. Architecture de confiance

```
Master Key PKA (HSM / YubiKey physique, hors ligne)
        │
        ├── dérive ──→ Clé de signing firmware (secp256r1)
        │
        └── dérive ──→ Clé de provisioning (AES-256)
                              │
                              ▼
              Injectée une fois par nœud au banc
                              │
              ┌───────────────┴───────────────┐
              │                               │
        Clé chiffrement SD              Clé identité nœud
        (AES-128, dérivée de              (HMAC, challenge-response
         provisioning + serial MCU)        pour auth Base Nexus P1)
```

- **Master Key PKA** : stockée hors ligne (YubiKey PIV ou HSM), jamais sur un nœud, jamais dans le dépôt.
- **Clé de provisioning** : dérivée de la Master Key via HKDF-SHA256 avec un sel fixe (ex. `"wildnexus-provisioning-v1"`). Cette clé AES-256 est utilisée uniquement au banc pour injecter les secrets par nœud.
- **Clé de chiffrement SD par nœud** : `AES-128_Key = HKDF-SHA256(Provisioning_Key, serial_MCU, "wildnexus-sd-encrypt-v1")`. Stockée en eFuse ESP32-S3 (bloc 0-1, 256 bits) ou OTP.
- **Clé d'identité nœud** : `HMAC_Key = HKDF-SHA256(Provisioning_Key, serial_MCU, "wildnexus-identity-v1")`. Utilisée pour l'authentification challenge-response avec la Base Nexus en P1. Stockée en eFuse.

### 2. Procédure de provisioning initial (banc / usine)

1. **Brancher le nœud en USB** (mode provisioning, firmware spécial).
2. **Lire le serial MCU** (unique, gravé usine Espressif).
3. **Dériver les clés** : le script de provisioning (laptop sécurisé) calcule `SD_Key` et `HMAC_Key` à partir de la `Provisioning_Key` (chargée depuis YubiKey) + `serial_MCU`.
4. **Graver en eFuse** : les 256 bits de `SD_Key` et `HMAC_Key` sont écrits dans les blocs eFuse ESP32-S3 (lecture seule après verrouillage).
5. **Verrouiller l'eFuse** : après écriture, les blocs sont verrouillés en lecture — aucune lecture logicielle possible, seul le moteur AES hardware y accède.
6. **Enregistrer le nœud** : le serial MCU est enregistré dans le registre de flotte (fichier chiffré hors dépôt), sans les clés elles-mêmes.
7. **Flasher le firmware de production** (sans les clés en clair — elles sont déjà en eFuse).

### 3. Cycle de vie des clés

| Phase | Action | Déclencheur |
|---|---|---|
| **Naissance** | Provisioning au banc (cf. §2) | Fabrication nœud |
| **Vie active** | Chiffrement/déchiffrement SD via moteur AES hardware, clé en eFuse | Usage terrain |
| **Rotation** | Regraver nouvelles clés si nœud reconditionné (effacement complet, re-provisioning) | Maintenance lourde, changement d'opérateur |
| **Révocation** | Désactiver le nœud dans le registre de flotte, clé marquée comme compromise | Perte, vol, suspicion de compromission |
| **Fin de vie** | Effacement complet eFuse (si supporté) + destruction physique SD + retrait registre | Retrait définitif |

### 4. Révocation et réponse à incident

Si un nœud est perdu, volé ou suspecté compromis :

1. **Révoquer dans le registre** : le serial MCU est marqué `REVOKED`. Les futures communications de ce nœud (P1 Base Nexus) sont rejetées.
2. **Impact limité** : grâce à la diversification, les autres nœuds restent protégés — leurs clés sont différentes.
3. **Rotation Master Key** : si la compromission suggère que la Master Key elle-même est menacée (ex. vol du laptop de provisioning), une nouvelle Master Key est générée, et tous les nœuds existants doivent être re-provisionnés. Ce scénario est P1/P2.

### 5. Stockage hors dépôt

- **Master Key** : YubiKey PIV ou HSM physique, coffre ignifugé.
- **Registre de flotte** : fichier chiffré (AES-256-GCM, clé dérivée d'une passphrase) listant `serial_MCU → date_provisioning → statut (actif/révoqué/fin_de_vie)`. Stocké dans `JCH_PRIVATE/`, exclu du dépôt Git via `.gitignore`.
- **Clés de provisioning** : jamais écrites sur disque en clair. Le script de provisioning les charge en RAM depuis YubiKey, les utilise, puis les efface.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| Clé maître unique en firmware | Très simple, pas de provisioning | 1 nœud dumpé = flotte entière compromise | Rejeté |
| Clé aléatoire par nœud, pas de master | Zéro risque master key | Impossible de re-provisionner un nœud sans effacer, pas de registre central | Rejeté |
| HKDF depuis master key YubiKey | Diversification, reproductible, master key hors ligne | Dépend d'un HSM physique, procédure banc | **Retenu** |
| TPM/ATECC608 externe | Sécurité maximale, stockage clé hardware dédié | Coût additionnel (~2 €/nœud), empreinte PCB, complexité I²C | Rejeté P0 (option P1 si exigé) |

## Conséquences

- WP03 firmware doit intégrer le moteur AES hardware ESP32-S3 pour chiffrement/déchiffrement SD avec clé eFuse.
- WP02 hardware : pas de composant additionnel en P0 (eFuse ESP32-S3 suffisant).
- WP04 tests doit inclure un test de provisioning complet (banc → eFuse → chiffrement → déchiffrement → vérification).
- ADR-010 (sécurité/RGPD) : dépend de cette ADR pour la diversification de clé (point de réserve R1).
- ADR-009 (architecture) : en P1, l'authentification nœud → Base Nexus utilisera la clé d'identité HMAC définie ici.
- Le registre de flotte (`JCH_PRIVATE/`) doit être créé avant le provisioning du premier prototype M-02.
- Un script de provisioning (`scripts/wildnexus_provision.py`) doit être développé avant M-02.

## Tests obligatoires avant acceptation

| Test | Critère |
|---|---|
| Provisioning complet banc | Serial MCU lu → clés dérivées → eFuse gravé → verrouillé |
| Chiffrement/Déchiffrement SD | Fichier écrit chiffré, relu déchiffré = identique |
| Diversification | Deux nœuds provisionnés → clés SD différentes confirmées |
| Lecture SD hors nœud | Carte SD montée sur PC → fichiers illisibles |
| Registre de flotte | Serial enregistré, statut actif, pas de clé en clair |
| Re-provisioning | Nœud reconditionné, nouvelles clés, anciennes inutilisables |

## Critère de révision

Réviser cette ADR si :
- le coût ou la disponibilité d'une YubiKey/HSM devient bloquant → évaluer HSM logiciel (age, SOPS) comme fallback ;
- un audit de sécurité externe exige un TPM/ATECC608 en P0 ;
- la procédure de provisioning banc s'avère trop lente pour 10+ prototypes → évaluer provisioning parallèle ou pré-gravure usine Espressif.

## Voir aussi

- [[ADR-010-securite-rgpd-edge-ai]] — exige la diversification de clé, point de réserve R1
- [[ADR-001-choix-mcu-p0]] — eFuse ESP32-S3, secure boot
- [[ADR-009-architecture-satellite-base-cloud]] — auth nœud → Base Nexus en P1
- [[WILDNEXUS_ENGINEERING_PHILOSOPHY]] — NN-09 Privacy by design
