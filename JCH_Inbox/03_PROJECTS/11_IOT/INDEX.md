# IOT — Index projet

> Projet ombrelle domotique JCH. Réorganisé le 2026-10-29 (bible V0 + nettoyage structure).
> **Source de vérité opérationnelle : `thread-iot.md`** (le reste s'aligne dessus).

## ⭐ Point d'entrée

- 🟢 **[IOT_DOSSIER_TECHNIQUE_V0.md](IOT_DOSSIER_TECHNIQUE_V0.md)** — **LA BIBLE** : référentiel technique consolidé + revue experts internes (Forge/Araignée/Atlas). *À lire en premier.*
- **[thread-iot.md](thread-iot.md)** — living doc : état opérationnel à jour (2026-10-22).
- **[executive-summary.md](executive-summary.md)** — résumé externe v2 (aligné, sans surpromesse).

## Nature & périmètre

- **Infrastructure personnelle** (pas de commercialisation).
- **4 nœuds** : `M5 Docker` (base/dev, Belgique) · `RPi 5 Esneux` (serre + maison) · `RPi 5 Van Lupo` (P0) · `RPi 5 Italie` (planifié).
- Autonome par site · supervision iPhone via **Tailscale** · **zéro cloud / zéro abonnement**.

## Sous-projets

| Projet | Hub / lieu | Statut |
|---|---|---|
| [`iot-van/`](iot-van/) | RPi 5 voiture (12V) — Westfalia Kelsey « Lupo » | 🔴 **P0 — deadline 15/12/2026** |
| [`iot-serre/`](iot-serre/) | RPi 5 Esneux | ⚪ gelé (reprise post-van) |
| [`iot-maison/`](iot-maison/) | même RPi Esneux | ⚪ ébauche long terme |
| [`_shared/`](_shared/) | — | ressources partagées (hub, procurement, capteurs) |

## Structure réelle (2026-10-29)

```
11_IOT/
├── INDEX.md                        ← ce fichier
├── IOT_DOSSIER_TECHNIQUE_V0.md      ← la bible
├── thread-iot.md                    ← living doc (source vérité)
├── executive-summary.md             ← résumé externe
├── iot-van/                         ← P0 Lupo
│   ├── ASSEMBLAGE-RPi5-VANLIFE.md · BOM-VANLIFE.md · scenarios-algorithmes-vanlife.md
│   ├── OPERATIONS-CAN-OBD.md · Liste/procédures/DIAGNOSTIC/POSTMORTEM (docs 2026-10)
│   ├── adr/ (ADR-001→006) · specs/ · ds300-tap/ · carplay/ · dashboard/
│   ├── enclosure/ · rpi-config/ · securite/obd/ · 99_REFERENCES/westfalia-kelsey/
│   └── passe-utile/{docs,briefs,boms}   (anciens docs consolidés)
├── iot-serre/ · iot-maison/
├── _shared/                        ← hub-esneux, procurement, paniers, convergence
├── PROTOCOLES/progress.md
├── guide installation HA/          ← guide (md/docx/pdf/png)
└── HISTORIQUE/                     ← notes datées 2026-07, 99_INBOX_NOTES, taches-annulees, Instagram
```

## État par site (source : thread 2026-10-22)

| Site | Statut |
|---|---|
| **Van Lupo** | RPi boot OK (SD 256 Go, HAOS 18.3) ; NVMe retiré ; alim **X1205→X1200** (achat différé) ; WiCAN Pro **installé** ; SNZB-02DR2 appairé ; RUT240 4G en stock ; reste 7 capteurs (~88 €) + X1200 |
| **Serre Esneux** | ⚪ gelé (post-van) — BOM 247 € prêt, hub Esneux 298 € |
| **Maison Esneux** | ⚪ ébauche |
| **Italie** | ⚪ planifié (RPi 5) |
| **M5 Docker** | 🟢 base/dev opérationnelle |

## Budget

- **Van** : ~1 026 € (BOM) — **reste réel court terme ≈ 150 €** (7 capteurs ~88 € + X1200 ~50-70 €). ⚠️ chiffres BOM (2026-07) périmés sur alim/stockage — voir bible §7.
- **Hub Esneux** : ~298 € (RPi 5 8 Go + X1201 + X1001 + SSD 128 Go).

## ⚠️ Chantiers bloquants (revue experts — cf. bible §16)

1. **`iot-van/ds300-tap/esphome-ds300.yaml`** : **GPIO8 utilisé 2×** (I²C SDA + relais) → à corriger avant flash.
2. **DC-DC USB-C PD 5 A absent du BOM** (exigé ADR-001) → X1200 5,1 V/5 A inatteignable sans lui.
3. **X1200 non vérifié** (datasheet, jauge I²C 0x32/0x36).
4. **Canal Zigbee** : 15 recouvre Wi-Fi 6 → choisir canal hors 1/6/11 (ex. 25).

## Spécialistes

- **Araignée 🕷️** — Zigbee/Z2M, ESPHome, capteurs
- **Forge 🛡️** — hardware, alimentation, ADR, CAN/OBD
- **Atlas 🗺️** — documentation, synthèse, cohérence
- **Vega** — architecture

---

*Généré par Dobby 🦉 — réorganisé 2026-10-29.*
