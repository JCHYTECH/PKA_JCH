# Liste capteurs — IOT Van (Lupo) — à commander

> **Date :** 2026-10-01 | **Orchestré par :** Dobby 🦉
> **Contexte initial :** RPi 5 réparé, HAOS 18.3, Zigbee opérationnel au 01/10. WiCAN Pro documenté comme physiquement installé.
> **Révision 2026-11-05 :** AirGuard Lupo = **SNZB-02UL** (van) ; AirGuard Serre = **SNZB-02DR2**. Le Zigbee du RPi est actuellement arrêté après déconnexion USB ; aucune donnée CAN n'est validée.
> **Source :** `BOM-capteurs-vanlife-enquete.md` (archivé), `hardware-state.md` et inventaire réel du 05/11.

---

## 0. Répartition des sources (important)

| Domaine | Source | Statut |
|---------|--------|--------|
| **Véhicule** (portes cabine, batterie 12V, vitesse, RPM, carburant, pneus, T°C moteur) | **WiCAN Pro (OBD/CAN)** | 🟡 matériel installé, données non validées |
| **Cellule** (porte coulissante, hayon, toit, frigo, mouvement, fuites) | **Zigbee** (ZBDongle-E) | à équiper ; service actuellement interrompu |

→ Les capteurs Zigbee visent la **cellule habitable**. Le WiCAN Pro ne couvre fonctionnellement le véhicule qu'après validation réseau, MQTT et entités réelles.

---

## 1. À COMMANDER — essentiel (P1)

### Capteurs d'ouverture — contact magnétique
| Usage | Qté | Modèle | Prix unit. |
|-------|-----|--------|-----------|
| Porte coulissante latérale | 1 | Aqara MCCGQ11LM (compact 41 mm) | ~8 € |
| Hayon arrière (unique) | 1 | Aqara MCCGQ11LM | ~8 € |
| Toit relevable (pop-top) | 1 | Sonoff SNZB-04P (CR2477, 5 ans) | ~9 € |
| Porte frigo | 1 | Sonoff SNZB-04P | ~9 € |

### Température / humidité
| Usage | Qté | Modèle | Prix unit. |
|-------|-----|--------|-----------|
| Cellule (T° + HR) | ✅ appareil affecté | **SNZB-02UL — AirGuard Lupo** ; service Zigbee à rétablir | — |
| Frigo (T° + HR) | à commander | **SNZB-02P**, inclus dans le panier final | ~12 € |

### Présence / mouvement (alarme)
| Usage | Qté | Modèle | Prix unit. |
|-------|-----|--------|-----------|
| Intérieur cellule | 1 | Aqara Motion Sensor P1 (ou Sonoff SNZB-03) | ~12 € |

### Sécurité additionnelle
| Usage | Qté | Modèle | Prix unit. |
|-------|-----|--------|-----------|
| Fuite d'eau (sous évier) | 1 | Aqara SJCGQ11LM | ~12 € |
| Vibration (anti-remorquage/tamper) | 1 | Aqara Vibration T1 | ~18 € |

### Éclairage hayon (barre LED 12V)
| Usage | Qté | Modèle | Prix unit. |
|-------|-----|--------|-----------|
| Contrôleur LED Zigbee 12V (RGBCCT, 5-24V DC, 6A) | 1 | GLEDOPTO GL-C-008S | ~15 € |
| Ruban LED COB 12V CCT (blanc chaud+froid) IP65, 5 m coupable | 1 | COB ~8W/m | ~18 € |

**Sous-total P1 : ~121 € estimés au 01/10** (10 articles, température frigo et éclairage hayon compris ; voir panier final).

---

## 2. Déjà reçu — NE PAS recommander

- Sonoff SNZB-02DR2 (T°/H°) → **AirGuard Serre** ✅ appairé
- Sonoff SNZB-02UL (T°/H° E-Ink) → **AirGuard Lupo** ✅ appairé
- Aqara Light Sensor T1 → luminosité
- Sonoff ZBMiniR2 → switch Zigbee
- Sonoff Smart Water Valve → électrovanne
- XKC-Y25-V ×4 → niveau cuves (eau propre/grise)
- Relais optocoupleur 12V ×3 → actionneurs
- INMP441 ×3 (dB) + MPU-6050 ×4 (inclinaison) → filaire
- Reolink Argus MagiCam → caméra/anti-intrusion
- WiCAN Pro → CAN/OBD véhicule

---

## 3. Plus tard (P3)

| Usage | Modèle | Prix | Note |
|-------|--------|------|------|
| Niveau gaz (bouteille **acier**) | Mopeka Pro Check | ~45 € | ✅ acier confirmé → Mopeka retenu |

---

## 4. Complétude par scénario

| Scénario | Capteurs | État |
|----------|----------|------|
| **Alarme intrusion** | Zigbee contact (cellule) + PIR + WiCAN (portes cabine) + Reolink | 🔶 à commander (contacts + PIR) |
| **Frigo** | contact porte frigo (SNZB-04P) + T°/H° à réaffecter | 🔶 à commander (contact + T°/H°) |
| **Batterie cellule** | UPS X1205 + accus + PV PI | ✅ reçu |
| **Batterie véhicule** | WiCAN Pro (SOC/courant/tension) | 🟡 matériel installé, entités non validées |
| **Cuves** | XKC-Y25-V ×4 | ✅ reçu |
| **Confort T°/H°** | SNZB-02UL (Lupo) + SNZB-02DR2 (Serre) + SNZB-02P (frigo) | 🔶 1 SNZB-02P à commander ; Zigbee à rétablir |
| **Éclairage hayon** | GLEDOPTO GL-C-008S + ruban COB 12V | 🔶 à commander |
| **Gaz** | Mopeka Pro Check | ⚪ P3 |
| **Inclinaison/assiette** | MPU-6050 | ✅ reçu |

---

## 5. Config confirmée (01/10)

1. ✅ Portes arrière : **hayon unique** → 1 contact
2. ✅ Bouteille de gaz : **acier** → Mopeka Pro Check (P3)
3. ✅ Toit relevable : **présent** → 1 contact toit

## 6. Panier final

| Réf | Qté | Total |
|-----|-----|-------|
| Aqara MCCGQ11LM (coulissante + hayon) | 2 | ~16 € |
| Sonoff SNZB-04P (toit + frigo) | 2 | ~18 € |
| Sonoff SNZB-02P (T°/H° frigo — réaffecté, à confirmer) | 1 | ~12 € |
| Aqara Motion P1 (mouvement) | 1 | ~12 € |
| Aqara SJCGQ11LM (fuite) | 1 | ~12 € |
| Aqara Vibration T1 (anti-remorquage) | 1 | ~18 € |
| GLEDOPTO GL-C-008S (contrôleur LED 12V) | 1 | ~15 € |
| Ruban LED COB 12V CCT IP65 (5 m) | 1 | ~18 € |
| **Total P1** | **10** | **~121 €** |
| Mopeka Pro Check (gaz, P3) | 1 | ~45 € |

---

*Liste générée par Dobby 🦉 — révisée le 2026-11-05. Les ~121 € sont des estimations historiques Amazon/AliExpress, non des devis actuels. X1200, DC-DC, silentblocs et coating sont suivis séparément dans `_shared/procurement-register.md`.*