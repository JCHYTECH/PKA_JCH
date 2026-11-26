# Bureau — refonte de l'alimentation (nettoyage du chaînage)

> **Date :** 2026-11-25 · **Statut :** planifié — achats à passer
> Objectif : supprimer le chaînage de multiprises, repartir sur 2 branches propres, intégrer le CPL sans risque.

---

## 1. Contexte

- **2 prises murales**, sur le **même disjoncteur 16 A** → **3680 W max partagé** (seuil prudent continu : ~2944 W).
- Chaînage actuel : multiprises en cascade → **à nettoyer**.
- **Charge estimée des appareils du bureau : ~219 W typique / ~399 W pic = 6–11 % du disjoncteur.**
  → **Aucun risque de surcharge.** Le risque réel = **les connexions** (cascade, contacts, multiprises bas de gamme), pas la puissance.

### Charge par appareil (estimations)

| Appareil | typ (W) | max (W) |
|---|---|---|
| M1 (MacBook Pro, Ollama) | 60 | 96 |
| M5 (MacBook Pro) | 60 | 100 |
| RPi Home (RPi5 HAOS) | 8 | 15 |
| RPi Lupo (RPi5 + ventilo + UPS HAT) | 15 | 40 |
| RE450 (répéteur) | 5 | 8 |
| TL-SG605E (switch) | 3 | 5 |
| CPL PA7017P (à venir) | 3 | 5 |
| EPSON ET-8550 (jet d'encre) | 2 | 25 |
| Écran LG UltraWide (M5) | 40 | 60 |
| Apple TV (AirPlay) | 3 | 5 |
| Divers (chargeurs, lampe) | 20 | 40 |
| **TOTAL** | **219** | **399** |

Marge libre ≈ **3280 W**. ⚠️ **Question ouverte** : existence d'un **gros appareil non listé** (chauffage d'appoint, bouilloire, imprimante laser, ampli) ? Si oui, le chiffrer.

---

## 2. Architecture cible (zéro cascade)

```
PRISE A (murale) ── CPL TL-PA7017P (direct, PASSIVE garantie)
                      ├─ port Gigabit ── Cat6 ── TL-SG605E ── M1 / RPi Home / RPi Lupo / RE450(AP)
                      └─ prise intégrée ── (petite multiprise PASSIVE) pour le cluster réseau basse conso
                                        OU rien (appareils réseau sur la prise B)

PRISE B (murale) ── multiprise PARAFOUDRE (interrupteur) ── MacBooks, écran LG, EPSON, chargeurs, divers
```

Règles d'or :
- **CPL jamais sur une multiprise parafoudrée** (le parafoudre filtre le signal CPL). CPL sur prise murale directe ou bloc **passif**.
- **Une seule multiprise par prise murale**, aucune cascade.
- Le parafoudre protège les appareils du poste (prise B) ; les RPis/switch peuvent y être aussi — seul le **CPL** doit rester sur la voie passive.

---

## 3. Liste d'achat (vérifiée amazon.com.be — prix au 25/11, volatils)

**Multiprise PARAFOUDRE — prise B (poste) :**
- **Perel PDU 8 prises, 16 A / 3680 W, parafoudre + interrupteur, style baie** — **€19,99** → https://www.amazon.com.be/dp/B00GMPRIAW  ⭐
- *alt :* Brennenstuhl Super-Solid 8 prises parafoudre + interrupteur — €23,31 → https://www.amazon.com.be/dp/B000YBXU6G

**Multiprise PASSIVE — prise A (réseau, si besoin) :**
- **Brennenstuhl ECO-LINE 8 prises, 3 m (gamme base, sans parafoudre)** — **€14,50** → https://www.amazon.com.be/dp/B00XUFBNW6
- *ou économique :* Zenitech 5 prises 16 A à interrupteur — €5,43 → https://www.amazon.com.be/dp/B077QSWBLY

**Rangement câbles :**
- **Boîte à câbles 2-pack + 12 attaches** — **€9,49** → https://www.amazon.com.be/dp/B0DSHYLT98

**CPL / réseau :**
- **CPL TP-Link TL-PA7017P (AV2, 1 Gigabit, prise pass-through)** — €26,90 → https://www.amazon.com.be/dp/B08CY2HDJS
- **Câble Cat6 court — DIGITUS Cat6A 1 m** — €2,29 → https://www.amazon.com.be/dp/B00GQUZRYM (×2)

**Total ≈ 75 €** (Perel + ECO-LINE + boîte + CPL + 2 câbles).

---

## 4. Plan d'installation

1. **Couper le disjoncteur** du bureau.
2. **Débrancher l'ancien chaînage** (multiprises en cascade) — repartir de zéro.
3. **Prise A** : brancher le **CPL PA7017P directement sur la prise murale** (passage pass-through conservé).
4. **Câble Cat6** : port Gigabit du CPL → port libre du **TL-SG605E**.
5. **Prise B** : brancher la **multiprise parafoudrée** ; y raccorder MacBooks (chargeurs), écran LG, EPSON, chargeurs divers.
6. **Cluster réseau** (RPi Home, RPi Lupo, TL-SG605E, RE450) : soit sur la prise intégrée du CPL via une petite multiprise **passive**, soit sur la prise B (parafoudre OK pour ces appareils). **Jamais le CPL sur le parafoudre.**
7. **Appairer le CPL** sur la même **clé réseau CPL** que le kit salon (bouton *Pair* ou utilitaire *tpPLC*).
8. **RE450 en mode AP** (uplink Ethernet via CPL) — app Tether → Mode → Point d'accès. Pas « répéteur Wi-Fi ».
9. **Ranger les câbles** (boîtes + attaches), dépoussiérer, vérifier fiches bien enfoncées.
10. **Vérifier le différentiel 30 mA** sur le circuit.
11. **Tests** : remettre le disjoncteur ; Dobby mesure **débit + jitter depuis M1** et vérifie M1/Home/Lupo.

---

## 5. Sécurité — à retenir

- **Pas de multiprises en cascade.** Une seule par prise.
- **CPL sur voie passive** uniquement (jamais sur parafoudre/filtre/onduleur).
- **Différentiel 30 mA** présent et fonctionnel.
- **Gros appareils thermiques** (chauffage, bouilloire) : hors de ce circuit.
- **Signaux d'alerte → électricien** : prise/fiche chaude, odeur de brûlé, décoloration, étincelles, disjoncteur qui saute.

---

## 6. Références

- Inventaire réseau : `JCH_Inbox/06_ADMIN/reseau/INDEX.md`
- Registre matériel : `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/hardware-state.md`
- Outil recherche produit : `bin/pka-amazon` (skill `amazon-be-search`)
